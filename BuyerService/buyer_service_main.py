import pika
from retry import retry
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

@retry(pika.exceptions.AMQPConnectionError, delay=5, jitter=(1, 3))
def get_connection():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host='rabbitmq',
            credentials=pika.PlainCredentials('guest', 'guest')
        )
    )
    return connection

def callback(ch, method, properties, body):
    buyer = body.decode()
    logging.info(f"Received buyer: {buyer}")



if __name__ == '__main__':
    connection = get_connection()
    channel = connection.channel()

    # Declare a direct exchange or the same exchange your producer uses
    channel.exchange_declare(exchange='buyers', exchange_type='direct')

    # Declare a queue for buyers
    queue_name = 'buyer_queue'
    channel.queue_declare(queue=queue_name, durable=True)  # Make the queue durable

    # Bind the queue to the exchange
    channel.queue_bind(exchange='buyers', queue=queue_name)

    logging.info('Waiting for buyers. To exit press CTRL+C')
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        logging.info("Stopping the consumer...")
    finally:
        channel.stop_consuming()
        connection.close()