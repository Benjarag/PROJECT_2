import pika
from retry import retry


class PaymentSender:
    def __init__(self) -> None:
        self.rabbitmq_connection = self.__get_connection()
        channel = self.rabbitmq_connection.channel()
        channel.exchange_declare(exchange='payment_exchange', exchange_type='fanout')
        channel.queue_declare(queue='email_order_payment')
        channel.queue_declare(queue='inventory_queue')
        channel.queue_bind(exchange='payment_exchange', queue='email_order_payment')
        channel.queue_bind(exchange='payment_exchange', queue='inventory_queue')

    def send_payment_event(self, payment_message):
        channel = self.rabbitmq_connection.channel()
        channel.basic_publish(exchange='payment_exchange', routing_key='', body=(payment_message))
        channel.close()

    @retry(pika.exceptions.AMQPConnectionError, delay=5, jitter=(1, 3))
    def __get_connection(self):
        return pika.BlockingConnection(pika.ConnectionParameters(
            "rabbitmq", credentials=pika.PlainCredentials('user', 'password'), heartbeat=600))
