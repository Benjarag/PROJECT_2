import pika
import json
from mail_sender import MailSender

class Message:
    def __init__(self, orderId, buyerMail, merchantMail, productName, totalPrice, state) -> None:
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
        self.waiting_messages = {}

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
            if orderId in self.waiting_messages:
                message = Message(
                    orderId, 
                    buyerEmail, 
                    merchantEmail, 
                    productName, 
                    totalPrice, 
                    self.waiting_messages[orderId][0])
                self.process_message(message)
            else:
                self.waiting_messages[orderId] = [buyerEmail, merchantEmail, productName, totalPrice]
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
            if orderId in self.waiting_messages:
                message = Message(
                    orderId, 
                    self.waiting_messages[orderId][0], 
                    self.waiting_messages[orderId][1], 
                    self.waiting_messages[orderId][2], 
                    self.waiting_messages[orderId][3], 
                    state)
                self.process_message(message)
            else:
                self.waiting_messages[orderId] = [state]
        except json.JSONDecodeError:
            pass
        except KeyError as e:
            pass
        finally:
            ch.basic_ack(delivery_tag=method.delivery_tag)

    def process_message(self, message: Message):
        mail_sender = MailSender
        mail_sender.send_email(message.buyerMail, 'Order has been created', f'{message.orderId}: {message.productName} {message.totalPrice}')
        mail_sender.send_email(message.merchantMail, 'Order has been created', f'{message.orderId}: {message.productName} {message.totalPrice}')
        if message.state == 'success':
            mail_sender.send_email(message.buyerMail, 'Order has been purchased', f'Order {message.orderId} has been successfully pruchased')
            mail_sender.send_email(message.merchantMail, 'Order has been purchased', f'Order {message.orderId} has been successfully pruchased')
        else:
            mail_sender.send_email(message.buyerMail, 'Order purchase failed', f'Order {message.orderId} purchase has failed')
            mail_sender.send_email(message.merchantMail, 'Order purchase failed', f'Order {message.orderId} purchase has failed')

    def start_consuming(self):

        def callback(ch, method, properties, body):
            if method.routing_key == self.order_queue:
                self.process_order(ch, method, properties, body)
            elif method.routing_key == self.payment_queue:
                self.process_payment(ch, method, properties, body)


        self.channel.basic_consume(queue=self.order_queue, on_message_callback=callback)
        self.channel.basic_consume(queue=self.payment_queue, on_message_callback=callback)

        print("Waiting for messages...")
        self.channel.start_consuming()
