from validation import Validate
from consume import PaymentConsumer

# from event_consumer import MailEventConsumer

def main():
    # Create a single instance of MailEventConsumer to avoid recreating it in each loop
    validator = Validate()
    consumer = PaymentConsumer()
    
    while True:
        consumer.start_consuming()
        validator.validate_all()

if __name__ == "__main__":
    main()
