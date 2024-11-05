import json

class BuyerSender:
    def __init__(self, connection):
        self.connection = connection

    def send_message(self, buyer: dict):
        channel = self.connection.channel()
        channel.basic_publish(
            exchange='buyer_updates',
            routing_key='',
            body=json.dumps(buyer)
        )
        print("Buyer update sent!")
