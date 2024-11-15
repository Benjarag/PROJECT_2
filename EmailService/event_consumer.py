import pika
from event_processor import MailEventProcessor
from retry import retry
import json

class NotificationEventConsumer:
    def __init__(self):
        self.message_broker_host = 'rabbitmq'
        self.purchase_queue = 'order_queue'
        self.transaction_queue = 'payment_queue'
        
        self.purchase_exchange = 'order_events'
        self.transaction_exchange = 'payment_events'

        self.broker_connection = self.__get_broker_connection()
        self.broker_channel = self.broker_connection.channel()

        self.broker_channel.exchange_declare(exchange=self.purchase_exchange, exchange_type='fanout')
        self.broker_channel.exchange_declare(exchange=self.transaction_exchange, exchange_type='fanout')
        
        self.broker_channel.queue_declare(queue=self.purchase_queue)
        self.broker_channel.queue_declare(queue=self.transaction_queue)
        
        self.broker_channel.queue_bind(exchange=self.purchase_exchange, queue=self.purchase_queue)
        self.broker_channel.queue_bind(exchange=self.transaction_exchange, queue=self.transaction_queue)

    def start_listening(self):
        def purchase_callback(channel, method, properties, body):
            notification_processor = MailEventProcessor()
            message_data = json.loads(body)
            print(f"Received Purchase-Created event: {message_data}")
            notification_processor.process_order(channel, method, properties, body)

        def transaction_callback(channel, method, properties, body):
            notification_processor = MailEventProcessor()
            message_data = json.loads(body)
            print(f"Received Transaction event: {message_data}")  
            notification_processor.process_payment(channel, method, properties, body)


        self.broker_channel.basic_consume(queue=self.purchase_queue, auto_ack=True, on_message_callback=purchase_callback)
        self.broker_channel.basic_consume(queue=self.transaction_queue, auto_ack=True, on_message_callback=transaction_callback)

        self.broker_channel.basic_qos(prefetch_count=1)
        print("NotificationService is now consuming messages...")
        self.broker_channel.start_consuming()

    @retry(pika.exceptions.AMQPConnectionError, delay=5, jitter=(1, 3))
    def __get_broker_connection(self):
        return pika.BlockingConnection(pika.ConnectionParameters(
            host=self.message_broker_host,
            credentials=pika.PlainCredentials("guest", "guest"),
            heartbeat=120
            ))
