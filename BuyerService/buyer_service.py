import pika

class BuyerSender:
    def __init__(self) -> None:
        self.connection = self.__get_connection()
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='buyer_events', exchange_type='fanout')

    def send_buyer_event(self, buyer):
        self.channel.basic_publish(exchange='buyer_events', routing_key='', body=buyer.json())

    def __get_connection(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', credentials=pika.PlainCredentials('guest', 'guest')))
        return connection