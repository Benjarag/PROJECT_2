# hér ætla ég að consume event, sem að order servcie gefur frá sér.
import pika
import json

class PaymentConsumer:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.payment_data = None 

    def callback(self, ch, method, properties, body):
        message = json.loads(body.decode())
        print(" [x] Received %r" % body)
        self.payment_data = json.loads(body)  # hér er hægt að vinna með upplýsingarnar sem order service sendir
        return message

    def start_consuming(self):
        self.channel.exchange_declare(queue='order_queue')
        self.channel.basic_consume(exchange='order_queue', exchange_type="fanout")

        routing_key = 'payment_queue'
        self.channel.queue_declare(queue=routing_key)
        self.channel.queue_bind(exchange='order_queue', queue=routing_key)
        self.channel.basic_consume(queue=routing_key, on_message_callback=self.callback, auto_ack=True) 
    
        print(" [*] Waiting for messages. To exit press CTRL+C")
        self.channel.start_consuming()
        

    def get_payment_data(self):
        return self.payment_data
    
    def get_order_id(self):
        self.order_id = self.payment_data.get("orderId") if self.payment_data else None
        return self.order_id