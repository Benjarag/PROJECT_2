import os
from sendgrid.helpers.mail import Mail
from sendgrid import SendGridAPIClient
from dotenv import load_dotenv

load_dotenv()

class MailSender:
    def send_email(self, to_email, subject, html_content):
        message = Mail(
            from_email=os.environ.get('SENDGRID_SENDER_MAIL'),
            to_emails=to_email,
            subject=subject,
            html_content=html_content)
        try:
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            response = sg.send(message)
        except Exception as e:
            pass




    