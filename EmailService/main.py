import os
from mail_sender import MailSender 

'''EKKI ACTUAL MAIN FILE. BARA TIL AÐ TESTA SMÁ'''
def main():
    recipient_email = 'haukurbesti@gmail.com'
    subject = 'DOCKER MAIL SENT'
    html_content = "<p>YOU DID IT BIH</p>"

    # Initialize the MailSender and send the email
    mail_sender = MailSender()
    mail_sender.send_email(to_email=recipient_email, subject=subject, html_content=html_content)
    print('Email sent succesfully...')

if __name__ == "__main__":
    main()

