import unittest
import json
import os
from email_producer import EmailOrderProducer, Message  # Adjust import as necessary
from mail_sender import MailSender  # Make sure this imports the SendGrid MailSender class

# Ensure SendGrid is properly configured in MailSender class
class TestEmailOrderProducer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Setup email configuration, replace with real emails for testing.
        cls.buyer_email = "your_buyer_email@example.com"
        cls.merchant_email = "your_merchant_email@example.com"
        
        # Initialize the EmailOrderProducer with direct SendGrid emailing.
        cls.email_producer = EmailOrderProducer(rabbitmq_host='localhost')  # Or your RabbitMQ setup
        
    def test_process_order_sends_emails(self):
        """Test if process_order correctly triggers emails."""
        message_data = {
            "orderId": 1,
            "buyerEmail": self.buyer_email,
            "merchantEmail": self.merchant_email,
            "productName": "Test Product",
            "totalPrice": 100.0
        }

        # Create message and simulate sending email
        message = Message(**message_data)
        self.email_producer.push_mail(message)  # Push the email manually to test

        # Log to console that the test email was sent (no assertions as this is a live email test)
        print("Test order email sent to:", self.buyer_email, self.merchant_email)

    def test_process_payment_success_sends_emails(self):
        """Test if process_payment success correctly triggers purchase success emails."""
        message_data = {
            "orderId": 1,
            "buyerMail": self.buyer_email,
            "merchantMail": self.merchant_email,
            "state": "success"
        }

        # Create message and simulate sending email
        message = Message(**message_data)
        self.email_producer.push_mail(message)

        # Log to console that the test email was sent
        print("Test payment success email sent to:", self.buyer_email, self.merchant_email)

    def test_process_payment_failure_sends_emails(self):
        """Test if process_payment failure correctly triggers purchase failure emails."""
        message_data = {
            "orderId": 1,
            "buyerMail": self.buyer_email,
            "merchantMail": self.merchant_email,
            "state": "failed"
        }

        # Create message and simulate sending email
        message = Message(**message_data)
        self.email_producer.push_mail(message)

        # Log to console that the test email was sent
        print("Test payment failure email sent to:", self.buyer_email, self.merchant_email)

if __name__ == "__main__":
    unittest.main()
