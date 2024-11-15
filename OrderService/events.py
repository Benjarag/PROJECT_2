import pika
import json
from retry import retry

RABBITMQ_HOST = "rabbitmq"

class EventManager:
    def __init__(self) -> None:
        self.connection = self.__get_connection()
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange="order_events", exchange_type="fanout")

    def publish_event(self, event_data: dict):
        self.channel.basic_publish(
        exchange="order_events",
        routing_key='',
        body=json.dumps(event_data)
        )

    @retry(pika.exceptions.AMQPConnectionError, delay=5, jitter=(1, 3))
    def __get_connection(self):
        return pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
