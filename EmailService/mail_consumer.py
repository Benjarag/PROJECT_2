import pika
import json
from mail_sender import MailSender
from models.order_mail import OrderMail
from models.payment_mail import PaymentMail


class MailEventConsumer:
    def __init__(self, rabbitmq_host='rabbitmq', order_queue='order_queue', payment_queue='payment_queue'):
        self.rabbitmq_host = rabbitmq_host
        self.order_queue = order_queue
        self.payment_queue = payment_queue
        self.mail_sender = MailSender

        #Rabbitmq
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.rabbitmq_host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.order_queue)
        self.channel.queue_declare(queue=payment_queue)
    
    '''Implementa hvernig messages eru processed'''
    def process_order(self, ch, method, properties, body):
        pass
        
    '''Implementa hvernig messages eru processed'''
    def process_payment(self, ch, method, properties, body):
        pass
    
    '''Implementa þegar það er ákveðið hvernig messages eru processed'''
    def push_order_mail(self, message: OrderMail):
        self.mail_sender.send_email()

    '''Implementa þegar það er ákveðið hvernig messages eru processed'''
    def push_payment_mail(self, message: PaymentMail):
        self.mail_sender.send_email()

    def start_consuming(self):

        def callback(ch, method, properties, body):
            if method.routing_key == self.order_queue:
                self.process_order(ch, method, properties, body)
            elif method.routing_key == self.payment_queue:
                self.process_payment(ch, method, properties, body)


        self.channel.basic_consume(queue=self.order_queue, on_message_callback=callback)
        self.channel.basic_consume(queue=self.payment_queue, on_message_callback=callback)


        self.channel.start_consuming()