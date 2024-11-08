import pika
from event_processor import MailEventProcessor
from retry import retry

class MailEventConsumer:
    def __init__(self, rabbitmq_host='rabbitmq', order_queue='order_queue', payment_queue='payment_queue'):
        self.rabbitmq_host = rabbitmq_host
        self.order_queue = order_queue
        self.payment_queue = payment_queue
        
        self.order_exchange = 'order_events'
        self.payent_exchange = 'payment_events'

        #Rabbitmq
        self.connection = self.__get_connection()
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=self.order_exchange, exchange_type='fanout')
        self.channel.exchange_declare(exchange=self.payent_exchange, exchange_type='fanout')
        
        self.channel.queue_declare(queue=self.order_queue)
        self.channel.queue_declare(queue=payment_queue)
        
        self.channel.queue_bind(exchange=self.order_exchange, queue=self.order_queue)
        self.channel.queue_bind(exchange=self.payent_exchange, queue=self.payment_queue)
    

    

    def start_consuming(self):

        def callback(ch, method, properties, body):
            mail_processor = MailEventProcessor
            if method.routing_key == self.order_queue:
                mail_processor.process_order(ch, method, properties, body)
            elif method.routing_key == self.payment_queue:
                mail_processor.process_payment(ch, method, properties, body)
            ch.basic_ack(delivery_tag=method.delivery_tag)


        self.channel.basic_consume(queue=self.order_queue, on_message_callback=callback)
        self.channel.basic_consume(queue=self.payment_queue, on_message_callback=callback)

        self.channel.basic_qos(prefetch_count=1)
        self.channel.start_consuming()

    @retry(pika.exceptions.AMQPConnectionError, delay=5, jitter=(1, 3))
    def __get_connection(self):
        return pika.BlockingConnection(pika.ConnectionParameters(host=self.rabbitmq_host))