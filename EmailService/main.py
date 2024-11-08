from event_consumer import MailEventConsumer


def main():
    while True:
        mail_consumer = MailEventConsumer
        mail_consumer.start_consuming()


if __name__ == "__main__":
    main()