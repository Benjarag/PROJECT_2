from models.order_mail import OrderMail
from models.payment_mail import PaymentMail
from mail_sender import MailSender
import json

class MailEventProcessor:
    def __init__(self) -> None:
        self.email_sender = MailSender()
    
    def handle_purchase_event(self, channel, delivery_method, msg_properties, msg_body):
        event_message = msg_body.decode()
        try:
            purchase_message = self._process_order_data(event_message)
            self.send_purchase_email(purchase_message)
        except json.JSONDecodeError:
            print("Failed to decode from JSON")
        except KeyError as e:
            print(f"Missing the key in event data: {e}")
        finally:
            print("Processing purchase event done")
    
    def handle_transaction_event(self, channel, delivery_method, msg_properties, msg_body):
        event_message = msg_body.decode()
        try:
            event_data = json.loads(event_message)
            transaction_id = event_data.get('orderId')
            transaction_state = event_data.get('state')
            transaction_message = PaymentMail(
                orderId=transaction_id,
                state=transaction_state
            )
            self.send_transaction_email(transaction_message)
        except json.JSONDecodeError:
            pass
        except KeyError as e:
            pass
        finally:
            pass
    
    def send_purchase_email(self, purchase_message: OrderMail):
        print(f"Sending email to buyer: {purchase_message.buyer_mail}")
        self.email_sender.send_email(
            to_email=purchase_message.buyer_mail, 
            subject='Order has been created',
            html_content=f'Order: {purchase_message.order_id}, Product: {purchase_message.product_name}, Price: ${purchase_message.product_price}'
        )
        print(f"Sending email to merchant: {purchase_message.merchant_mail}")
        self.email_sender.send_email(
            to_email=purchase_message.merchant_mail, 
            subject='Order has been created',
            html_content=f'Order: {purchase_message.order_id}, Product: {purchase_message.product_name}, Price: ${purchase_message.product_price}'
        )
        

    def send_transaction_email(self, transaction_message: PaymentMail):
        if transaction_message.state == 'successful':
            self.email_sender.send_email(
                to_email=transaction_message.merchantMail, 
                subject='Order has been purchased',
                html_content=f'Order {transaction_message.orderId} has been successfully purchased'
            )
            self.email_sender.send_email(
                to_email=transaction_message.buyerMail, 
                subject='Order has been purchased',
                html_content=f'Order {transaction_message.orderId} has been successfully purchased'
            )
        elif transaction_message.state == 'failed':
            self.email_sender.send_email(
                to_email=transaction_message.merchantMail, 
                subject='Order purchase failed',
                html_content=f'Order {transaction_message.orderId} has failed'
            )
            self.email_sender.send_email(
                to_email=transaction_message.buyerMail, 
                subject='Order purchase failed',
                html_content=f'Order {transaction_message.orderId} purchase has failed'
            )
        else:
            raise json.JSONDecodeError

