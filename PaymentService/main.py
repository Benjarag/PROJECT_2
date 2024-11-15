from fastapi import FastAPI
import pika
import json
from payment_service import PaymentService

app = FastAPI()
payment_service = PaymentService(rabbitmq_url="rabbitmq")

def consume_order_created():
    connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
    channel = connection.channel()
    channel.queue_declare(queue="order_created")

    def callback(ch, method, properties, body):
        order_event = json.loads(body)
        payment_service.process_order_created(order_event)

    channel.basic_consume(queue="order_created", on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

@app.on_event("startup")
async def startup_event():
    consume_order_created()
