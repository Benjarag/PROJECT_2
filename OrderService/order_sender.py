import pika

class OrderSender:
    def __init__(self) -> None:
        self.connection = self.__get_connection()
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='order_events', exchange_type='fanout')

    def send_order_event(self, order):
        self.channel.basic_publish(exchange='order_events', routing_key='', body=order.json())

    def __get_connection(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', credentials=pika.PlainCredentials('guest', 'guest')))
        return connection
