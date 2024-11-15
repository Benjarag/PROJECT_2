import pika
from event_processor import MailEventProcessor
from retry import retry
import json

class MailEventConsumer:
    def __init__(self):
        self.rabbitmq_host = 'rabbitmq'
        self.order_queue = 'order_queue'
        self.payment_queue = 'payment_queue'
        
        self.order_exchange = 'order_events'
        self.payent_exchange = 'payment_events'

        self.connection = self.__get_connection()
        self.channel = self.connection.channel()

        self.channel.exchange_declare(exchange=self.order_exchange, exchange_type='fanout')
        self.channel.exchange_declare(exchange=self.payent_exchange, exchange_type='fanout')
        
        self.channel.queue_declare(queue=self.order_queue)
        self.channel.queue_declare(queue=self.payment_queue)
        
        self.channel.queue_bind(exchange=self.order_exchange, queue=self.order_queue)
        self.channel.queue_bind(exchange=self.payent_exchange, queue=self.payment_queue)

    def start_consuming(self):
        def order_callback(ch, method, properties, body):
            mail_processor = MailEventProcessor()
            data = json.loads(body)
            print(f"Received Order-Created event: {data}")
            mail_processor.process_order(ch, method, properties, body)

        def payment_callback(ch, method, properties, body):
            mail_processor = MailEventProcessor()
            data = json.loads(body)
            print(f"Received Payment event: {data}")  
            mail_processor.process_payment(ch, method, properties, body)


        self.channel.basic_consume(queue=self.order_queue, auto_ack=True, on_message_callback=order_callback)
        self.channel.basic_consume(queue=self.payment_queue, auto_ack=True, on_message_callback=payment_callback)

        self.channel.basic_qos(prefetch_count=1)
        print("EmailService is now consuming messages...")
        self.channel.start_consuming()

    @retry(pika.exceptions.AMQPConnectionError, delay=5, jitter=(1, 3))
    def __get_connection(self):
        return pika.BlockingConnection(pika.ConnectionParameters(
            host=self.rabbitmq_host,
            credentials=pika.PlainCredentials("guest", "guest"),
            heartbeat=120
            ))