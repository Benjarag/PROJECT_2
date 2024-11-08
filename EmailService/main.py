from event_consumer import MailEventConsumer

def main():
    # Create a single instance of MailEventConsumer to avoid recreating it in each loop
    mail_consumer = MailEventConsumer()
    
    while True:
        mail_consumer.start_consuming()

if __name__ == "__main__":
    main()
