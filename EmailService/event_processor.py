from models.order_mail import OrderMail
from models.payment_mail import PaymentMail
from mail_sender import MailSender
import json

class MailEventProcessor:
    def __init__(self) -> None:
        self.mail_sender = MailSender()
    
    def process_order(self, ch, method, properties, body):
        message = body.decode()
        try:
            data = json.loads(message)
            order_id = data.get('order_id')
            buyer_mail = data.get('buyer_mail')
            merchant_mail = data.get('merchant_mail')
            product_name = data.get('product_name')
            product_price = data.get('total_price') or 0
            card_number = data.get('card_number')
            year_expiration = data.get('year_expiration')
            month_expiration = data.get('month_expiration')
            cvc = data.get('cvc')
            
            order_message = OrderMail(
                order_id=order_id,
                buyer_mail=buyer_mail,
                merchant_mail=merchant_mail,
                product_name=product_name,
                product_price=product_price,
                card_number=card_number,
                year_expiration=year_expiration,
                month_expiration=month_expiration,
                cvc=cvc
            )
            self.push_order_mail(order_message)
        except json.JSONDecodeError:
            print("Failed to decode JSON")
        except KeyError as e:
            print(f"Missing key in event data: {e}")
        finally:
            print("Finished processing order event")
    
    def process_payment(self, ch, method, properties, body):
        message = body.decode()
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
        print(f"Sending email to buyer: {message.buyer_mail}")
        self.mail_sender.send_email(
            to_email=message.buyer_mail, 
            subject='Order has been created',
            html_content=f'Order: {message.order_id} {message.product_name} ${message.product_price}'
        )
        print(f"Sending email to merchant: {message.merchant_mail}")
        self.mail_sender.send_email(
            to_email=message.merchant_mail, 
            subject='Order has been created',
            html_content=f'Order: {message.order_id} {message.product_name} ${message.product_price}'
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