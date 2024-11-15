
import pika
import json
from inventory_repository import InventoryRepository
from pydantic import BaseModel

class InventoryCreateRequest(BaseModel):
    merchantId: int
    productName: str
    price: float
    quantity: int
    reserved: int = 0 

product_repo = InventoryRepository(file_path='./data/inventory.json')

def consume_payment_event(ch, method, properties, body):
    event_data = json.loads(body)
    order_id = event_data['orderId']
    status = event_data['status'] 
    product_id = event_data['product_id']  

    try:
        if status == "success":
            updated_product_id, updated_product = product_repo.update_product_on_payment(product_id, payment_success=True)
            print(f"Payment successful for order {order_id}. Product {updated_product_id} updated: {updated_product}")
        
        elif status == "fail":
            updated_product_id, updated_product = product_repo.update_product_on_payment(product_id, payment_success=False)
            print(f"Payment failed for order {order_id}. Product {updated_product_id} reverted: {updated_product}")
        else:
            raise ValueError(f"Invalid status for order {order_id}: {status}")

        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"Error processing order {order_id}: {str(e)}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

def start_consuming():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    channel.queue_declare(queue='payment_queue', durable=True)

    channel.basic_consume(queue='payment_queue', on_message_callback=consume_payment_event)

    print("Inventory Service is waiting for messages...")
    channel.start_consuming()
