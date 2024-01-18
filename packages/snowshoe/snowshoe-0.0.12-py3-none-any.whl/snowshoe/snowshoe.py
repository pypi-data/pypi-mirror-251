import functools
import json
import threading
from enum import Enum
from threading import Thread
from typing import Callable

import pika
from pika import exceptions
from pika.exchange_type import ExchangeType
from retry import retry


class AckMethod(Enum):
    OFF = 0
    INSTANTLY = 1
    AUTO = 2


class FailureMethod(Enum):
    DROP = 0
    REQUEUE = 1
    DLX = 2


class QueueBinding:
    exchange: str
    routing_key: str

    def __init__(self, exchange: str, routing_key: str = '*') -> None:
        self.exchange = exchange
        self.routing_key = routing_key


class Queue:

    name: str
    bindings: list[QueueBinding]
    passive = False
    durable = False
    exclusive = False
    auto_delete = False
    failure_method = FailureMethod.DROP

    def __init__(
            self,
            name: str,
            bindings: list[QueueBinding] = None,
            failure_method=FailureMethod.DROP,
            passive=False,
            durable=False,
            exclusive=False,
            auto_delete=False,
    ) -> None:
        self.name = name
        self.bindings = bindings or []
        self.passive = passive
        self.durable = durable
        self.exclusive = exclusive
        self.auto_delete = auto_delete
        self.failure_method = failure_method


class Message:
    data: dict
    delivery_tag: int
    topic: str

    def __init__(self, data: dict, delivery_tag: int, topic: str) -> None:
        self.data = data
        self.delivery_tag = delivery_tag
        self.topic = topic


class Snowshoe:
    consumer_connection: pika.BlockingConnection
    publisher_connection: pika.BlockingConnection
    consumer_channel: pika.adapters.blocking_connection.BlockingChannel
    producer_channel: pika.adapters.blocking_connection.BlockingChannel
    name: str

    def __init__(
            self,
            name: str,
            host: str = '127.0.0.1',
            port: int = 5672,
            username: str = None,
            password: str = None,
            vhost: str = '/'
    ) -> None:
        self.name = name
        self.consumer_connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=host,
            port=port,
            virtual_host=vhost,
            credentials=pika.PlainCredentials(
                username=username,
                password=password
            )
        ))
        self.producer_connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=host,
            port=port,
            virtual_host=vhost,
            credentials=pika.PlainCredentials(
                username=username,
                password=password
            )
        ))
        self.consumer_channel = self.consumer_connection.channel()
        self.producer_channel = self.producer_connection.channel()
        self.producer_channel.exchange_declare(self.name, ExchangeType.topic)
        self._threads: list[Thread] = []
        self._queues: dict[str, Queue] = {}

    @retry(exceptions.AMQPConnectionError, delay=5, jitter=(1, 3))
    def run(self):
        try:
            self.consumer_channel.start_consuming()
        except KeyboardInterrupt:
            self.consumer_channel.stop_consuming()

        for thread in self._threads:
            thread.join()

    def define_queues(self, queues: list[Queue]):
        self.consumer_channel.exchange_declare('_failed_messages_dlx', ExchangeType.topic)

        for queue in queues:
            self._queues[queue.name] = queue
            queue_name = self.name + ':' + queue.name
            if queue.failure_method == FailureMethod.DLX:
                arguments = {'x-dead-letter-exchange': '_failed_messages_dlx'}
            else:
                arguments = None
            self.consumer_channel.queue_declare(
                queue_name,
                passive=queue.passive,
                durable=queue.durable,
                exclusive=queue.exclusive,
                auto_delete=queue.auto_delete,
                arguments=arguments
            )
            for binding in queue.bindings:
                self.consumer_channel.exchange_declare(binding.exchange, ExchangeType.topic)
                self.consumer_channel.queue_bind(queue_name, binding.exchange, binding.routing_key)

    def emit(self, topic: str, data: dict, ttl: int = None):
        return self.producer_channel.basic_publish(
            exchange=self.name,
            routing_key=topic,
            body=json.dumps(data).encode(),
            properties=pika.BasicProperties(
                content_type='application/json',
                expiration=ttl
            )
        )

    def ack(self, delivery_tag: int = 0, multiple=False):
        self.consumer_channel.connection.add_callback_threadsafe(
            functools.partial(self.consumer_channel.basic_ack, delivery_tag, multiple)
        )

    def nack(self, delivery_tag: int = 0, multiple=False, requeue=True):
        self.consumer_channel.connection.add_callback_threadsafe(
            functools.partial(self.consumer_channel.basic_nack, delivery_tag, multiple, requeue)
        )

    def on(self, queue: str | Queue, ack_method: AckMethod = AckMethod.AUTO):
        if isinstance(queue, str):
            queue = self._queues.get(queue)

        if not isinstance(queue, Queue):
            raise Exception('Invalid Queue')

        def wrapper(handler: Callable[[Message], any]):

            def do_works(
                    _channel: pika.adapters.blocking_connection.BlockingChannel,
                    method: pika.spec.Basic.Deliver,
                    _properties: pika.spec.BasicProperties,
                    body: bytes
            ):
                try:
                    print(threading.get_ident())
                    message = Message(data=json.loads(body), topic=method.routing_key, delivery_tag=method.delivery_tag)
                    result = handler(message)
                    if ack_method == AckMethod.AUTO:
                        self.ack(method.delivery_tag)
                    return result
                except Exception as e:
                    if ack_method == AckMethod.AUTO:
                        self.nack(method.delivery_tag, requeue=queue.failure_method == FailureMethod.REQUEUE)
                    raise e

            def callback(*args, **kwargs):
                thread = Thread(target=do_works, args=args, kwargs=kwargs)
                self._threads.append(thread)
                thread.start()
                return thread

            self.consumer_channel.basic_consume(
                queue=self.name + queue.name,
                on_message_callback=callback,
                auto_ack=ack_method == AckMethod.INSTANTLY
            )

        return wrapper
