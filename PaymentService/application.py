import json
from container import Container
import pika
from payment_repository import PaymentRepository
from payment_event_sender import PaymentSender
from payment_validator import PaymentValidator
from retry import retry


@retry(pika.exceptions.AMQPConnectionError, delay=5, jitter=(1, 3))
def get_connection():
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        "rabbitmq", credentials=pika.PlainCredentials('user', 'password')))
    return connection.channel()


def callback(ch, method, properties, body):
    order_event = json.loads(body.decode())
    payment_result = payment_validator.validator(order_event["credit_card"])
    payment_repository.save_payment_results(payment_result, order_event["order_id"])
    order_event["payment_result"] = payment_result
    payment_event_sender.send_payment_event(json.dumps(order_event))


if __name__ == '__main__':
    container = Container()

    payment_repository: PaymentRepository = container.payment_repository_provider()
    payment_event_sender: PaymentSender = container.payment_sender_provider()
    payment_validator: PaymentValidator = container.payment_validator_provider()
    channel = get_connection()
    channel.queue_declare(queue='payment_order_create')

    channel.basic_consume(
                    queue='payment_order_create',
                    auto_ack=True,
                    on_message_callback=callback)

    channel.start_consuming()
