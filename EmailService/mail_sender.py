import os
from sendgrid.helpers.mail import Mail
from sendgrid import SendGridAPIClient



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
            #print(response.status_code)
            #print(response.body)
            #print(response.headers)
        except Exception as e:
            #print(e.body)
            pass



if __name__ == '__main__':
    email_sender = MailSender()
    email_sender.send_email('sindrib23@ru.is', 'testing', 'this is a test email')
    email_sender.send_email('oliver23@ru.is', 'testing', 'this is a test email')
    email_sender.send_email('benjaminr23@ru.is', 'testing', 'this is a test email')