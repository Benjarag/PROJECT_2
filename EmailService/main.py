from event_consumer import MailEventConsumer

def main():
    mail_consumer = MailEventConsumer()
    
    while True:
        mail_consumer.start_consuming()

if __name__ == "__main__":
    main()
