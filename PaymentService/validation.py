import json
from consume import PaymentConsumer
import pika

card_data = PaymentConsumer.get_payment_data() # hér eru upl. frá order service í 'VONA ÉG' réttu formatti


class Validate:

    def validate_cardNumber(self, card_number: str) -> bool:
        card_number = card_number.replace(" ", "")
        if len(card_number) != 16:
            return False
        
        total_sum = 0
        for i in range(16):
            digit = int(card_number[i])
            if i % 2 == 0:
                digit *= 2
                if digit > 9:
                    digit -= 9
            total_sum += digit
        return total_sum % 10 == 0

    def validate_year(self, card_year: str) -> bool:
        card_number = card_number.replace(" ", "")
        return len(card_year) == 4

    def validate_month(self, card_month: str) -> bool:
        card_number = card_number.replace(" ", "")
        month = int(card_month)
        return 1 <= month <= 12

    def validate_cvc(self, card_cvc: str) -> bool:
        card_number = card_number.replace(" ", "")
        return len(card_cvc) == 3

    def validate_all(self, card_data) -> bool:
        if self.validate_cardNumber(card_data["card_number"]) == False:
            return "fail"
        elif self.validate_year(card_data["year_expiration"]) == False:
            return "fail"
        elif self.validate_month(card_data["month_expiration"]) == False:
            return "fail"
        elif self.validate_cvc(card_data["cvc"]) == False:
            return "fail"
    
        return "success"
    
        # return (
        #     self.validate_cardNumber(card_data["cardNumber"]) and
        #     self.validate_year(card_data["year"]) and
        #     self.validate_month(card_data["month"]) and
        #     self.validate_cvc(card_data["cvc"])
        # )
    

# hér vill ég síðan búa til event sem að inventory- og email service geta consume-að
# þegar validation er complete, sem gefur annaðhvort paymentfail eða paymentcomplete

# event_type-ið er þá það sem validate_all skilar 

def publish_event(event_type, message):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=event_type)
    channel.exchange_declare(exchange='payment_events', exchange_type='fanout')
    channel.basic_publish(exchange='payment_events', routing_key=event_type, body=json.dumps(message))
    connection.close()

validation_result = Validate().validate_all(card_data)

if validation_result == "success":
    publish_event('paymentComplete', {'status': 'success', 'orderId': f"{PaymentConsumer.get_order_id()}"})
else:
    publish_event('paymentFailed', {'status': 'fail', 'card_data': f"{PaymentConsumer.get_order_id()}"})