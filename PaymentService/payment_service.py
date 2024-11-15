import pika
import json
from .utils import validate_card
from .payment_repository import PaymentRepository

class PaymentService:
    def __init__(self, rabbitmq_url: str):
        self.rabbitmq_url = rabbitmq_url
        self.repository = PaymentRepository()

    def process_order_created(self, order_event: dict):
        card_info = order_event["credit_card"]
        if validate_card(card_info["number"], card_info["month"], card_info["year"], card_info["cvc"]):
            result = "Payment-Successful"
        else:
            result = "Payment-Failure"

        self.repository.save_payment_result(order_event["order_id"], result)
        self.publish_event(order_event["order_id"], result)

    def publish_event(self, order_id: str, result: str):
        connection = pika.BlockingConnection(pika.ConnectionParameters(self.rabbitmq_url))
        channel = connection.channel()
        channel.queue_declare(queue="payment_results")
        channel.basic_publish(exchange="", routing_key="payment_results", body=json.dumps({"order_id": order_id, "result": result}))
        connection.close()
