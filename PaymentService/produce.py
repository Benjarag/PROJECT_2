import pika
from validation import Validate
from consume import PaymentConsumer




payment_data = PaymentConsumer().get_payment_data()

check = Validate().validate_all(payment_data)

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'), credentials= pika.PlainCredentials('guest', 'guest'))

channel = connection.channel()

channel.queue_declare(queue='PaymentService')

channel.basic_publish(exchange='', routing_key='PaymentService', body=f'{check}')
print(f" [x] Sent Validation Confirmation: {check}")

connection.close()