import pika
import json
from mail_sender import MailSender

class Message:
    def __init__(self, orderId, buyerMail, merchantMail, productName=None, totalPrice=None, state=None) -> None:
        self.orderId = orderId
        self.buyerMail = buyerMail
        self.merchantMail = merchantMail
        self.productName = productName
        self.totalPrice = totalPrice
        self.state = state


class EmailOrderProducer:
    def __init__(self, rabbitmq_host='rabbitmq', order_queue='order_queue', payment_queue='payment_queue') -> None:
        self.rabbitmq_host = rabbitmq_host
        self.order_queue = order_queue
        self.payment_queue = payment_queue

        #Rabbitmq
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.rabbitmq_host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.order_queue)
        self.channel.queue_declare(queue=payment_queue)
    
    def process_order(self, ch, method, properties, body):
        event = body.decoded()
        try:
            data = json.loads(event)
            orderId = data.get('orderId')
            buyerEmail = data.get('buyerEmail')
            merchantEmail = data.get('merchantEmail')
            productName = data.get('productName')
            totalPrice = data.get('totalPrice')
            message = Message(
                orderId=orderId, 
                buyerMail=buyerEmail, 
                merchantMail=merchantEmail, 
                productName=productName, 
                totalPrice=totalPrice)
            self.push_mail(message)
        except json.JSONDecodeError:
            pass
        except KeyError as e:
            pass
        finally:
            ch.basic_ack(delivery_tag=method.delivery_tag)

    
    
    def process_payment(self, ch, method, properties, body):
        event = body.decoded()
        try:
            data = json.loads(event)
            orderId = data.get('orderId')
            state = data.get('state')
            buyerMail = data.get('buyerEmail')
            merchantMail = data.get('merchantEmail')
            message = Message(orderId=orderId, buyerMail=buyerMail, merchantMail=merchantMail, state=state)
            self.push_mail(message)
        except json.JSONDecodeError:
            pass
        except KeyError as e:
            pass
        finally:
            ch.basic_ack(delivery_tag=method.delivery_tag)

    

    def push_mail(self, message: Message):
        mail_sender = MailSender
        if message.state is None:
            mail_sender.send_email(message.buyerMail, "Order has been created", f'Order: {message.orderId} {message.productName} for ${message.totalPrice}')
            mail_sender.send_email(message.merchantMail, "Order has been created", f'Order: {message.orderId} {message.productName} for ${message.totalPrice}')
        else:
            if message.state == 'success':
                mail_sender.send_email(message.buyerMail, 'Order has been purchased', f"Order {message.orderId} has been successfully purchased")
                mail_sender.send_email(message.merchantMail, 'Order has been purchased', f"Order {message.orderId} has been successfully purchased")
            else:
                mail_sender.send_email(message.buyerMail, "Order purchase failed", f"Order {message.orderId} purchase has failed")
                mail_sender.send_email(message.merchantMail, "Order purchase failed", f"Order {message.orderId} purchase has failed")
        

    def start_consuming(self):

        def callback(ch, method, properties, body):
            if method.routing_key == self.order_queue:
                self.process_order(ch, method, properties, body)
            elif method.routing_key == self.payment_queue:
                self.process_payment(ch, method, properties, body)


        self.channel.basic_consume(queue=self.order_queue, on_message_callback=callback)
        self.channel.basic_consume(queue=self.payment_queue, on_message_callback=callback)


        self.channel.start_consuming()




