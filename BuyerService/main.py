import pika
from retry import retry
import logging

# Set up logging for BuyerService
logging.basicConfig(level=logging.INFO)

@retry(pika.exceptions.AMQPConnectionError, delay=5, jitter=(1, 3))
def get_connection():
    """
    Establish a connection to RabbitMQ with retries.
    """
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host='rabbitmq',
            credentials=pika.PlainCredentials('guest', 'guest')
        )
    )
    return connection

def callback(ch, method, properties, body):
    """
    Process incoming buyer message.
    """
    buyer = body.decode()
    logging.info(f"Received buyer: {buyer}")
    # Add code to process the buyer data (e.g., save to a database)
    # Uncomment the next line if manual acknowledgment is needed
    # ch.basic_ack(delivery_tag=method.delivery_tag)

if __name__ == '__main__':
    connection = get_connection()
    channel = connection.channel()

    # Declare an exchange for buyers if different from orders
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
