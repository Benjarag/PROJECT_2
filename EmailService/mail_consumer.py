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
    

    def process_order(self, ch, method, properties, body):
        message = body.decoded()
        try:
            data = json.loads(message)
            orderId = data.get('orderId')
            buyerMail = data.get('buyerMail')
            merchantMail = data.get('merchantMail')
            productName = data.get('productName')
            totalPrice = data.get('totalPrice')
            order_message = OrderMail(
                orderId=orderId, 
                buyerMail=buyerMail, 
                merchantMail=merchantMail, 
                productName=productName, 
                totalPrice=totalPrice
            )
            self.push_order_mail(order_message)
        except json.JSONDecodeError:
            pass
        except KeyError as e:
            pass
        finally:
            pass
    
        

    def process_payment(self, ch, method, properties, body):
        message = body.decoded()
        try:
            data = json.loads(message)
            orderId = data.get('orderId')
            state = data.get('state')
            payment_message=PaymentMail(
                orderId=orderId,
                state=state
            )
            self.push_payment_mail(payment_message)
        except json.JSONDecodeError:
            pass
        except KeyError as e:
            pass
        finally:
            pass
    

    def push_order_mail(self, message: OrderMail):
        self.mail_sender.send_email(
            to_email=message.buyerMail, 
            subject='Order has been created',
            html_content=f'Order: {message.orderId} {message.productName} ${message.totalPrice}'
        )
        self.mail_sender.send_email(
            to_email=message.merchantMail, 
            subject='Order has been created',
            html_content=f'Order: {message.orderId} {message.productName} ${message.totalPrice}'
        )
        


    def push_payment_mail(self, message: PaymentMail):
        if message.state == 'successful':
            self.mail_sender.send_email(
                to_email=message.merchantMail, 
                subject='Order has been purchased',
                html_content=f'Order {message.orderId} has been successfully purchased'
            )
            self.mail_sender.send_email(
                to_email=message.buyerMail, 
                subject='Order has been purchased',
                html_content=f'Order {message.orderId} has been successfully purchased'
            )
        elif message.state == 'failed':
            self.mail_sender.send_email(
                to_email=message.merchantMail, 
                subject='Order purchase failed',
                html_content=f'Order {message.orderId} has been successfully purchased'
            )
            self.mail_sender.send_email(
                to_email=message.buyerMail, 
                subject='Order purchase failed',
                html_content=f'Order {message.orderId} purchase has failed'
            )
        else:
            raise json.JSONDecodeError

    def start_consuming(self):

        def callback(ch, method, properties, body):
            if method.routing_key == self.order_queue:
                self.process_order(ch, method, properties, body)
            elif method.routing_key == self.payment_queue:
                self.process_payment(ch, method, properties, body)


        self.channel.basic_consume(queue=self.order_queue, on_message_callback=callback)
        self.channel.basic_consume(queue=self.payment_queue, on_message_callback=callback)


        self.channel.start_consuming()