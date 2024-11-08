import pika
from event_processor import MailEventProcessor


class MailEventConsumer:
    def __init__(self, rabbitmq_host='rabbitmq', order_queue='order_queue', payment_queue='payment_queue'):
        self.rabbitmq_host = rabbitmq_host
        self.order_queue = order_queue
        self.payment_queue = payment_queue

        #Rabbitmq
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.rabbitmq_host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.order_queue)
        self.channel.queue_declare(queue=payment_queue)
    

    

    def start_consuming(self):

        def callback(ch, method, properties, body):
            mail_processor = MailEventProcessor
            if method.routing_key == self.order_queue:
                mail_processor.process_order(ch, method, properties, body)
            elif method.routing_key == self.payment_queue:
                mail_processor.process_payment(ch, method, properties, body)


        self.channel.basic_consume(queue=self.order_queue, on_message_callback=callback)
        self.channel.basic_consume(queue=self.payment_queue, on_message_callback=callback)


        self.channel.start_consuming()