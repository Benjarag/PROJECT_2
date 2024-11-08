import pika
import json



def publish_event(event_data: dict):
    RABBITMQ_HOST = "rabbitmq"

    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()

    channel.exchange_declare(exchange="order_events", exchange_type="fanout")

    channel.basic_publish(
        exchange="order_events",
        body=json.dumps(event_data)
    )

    print(f"Publishing order-event with order id: {event_data.order_id}")

    connection.close()
