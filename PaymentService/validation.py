import json
import pika
import threading
from consume import PaymentConsumer

card_data = PaymentConsumer.get_payment_data() # hér eru upl. frá order service í 'VONA ÉG' réttu formatti
consumer = PaymentConsumer()

def start_consuming():
    consumer.start_consuming()

thread = threading.Thread(target=start_consuming)
thread.start()

payment_data = PaymentConsumer.get_payment_data()
if payment_data: 
    credit_card_info = payment_data["card_number"] 
    year_info = payment_data["year_expiration"]
    month_info = payment_data["month_expiration"]
    cvc_info = payment_data["cvc"]
    order_id = payment_data["order_id"]
else:
    pass

class Validate:

    global credit_card_info, year_info, month_info, cvc_info, order_id

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

    def validate_all(self) -> bool:
        if self.validate_cardNumber(credit_card_info) == False:
            return "fail"
        elif self.validate_year(year_info) == False:
            return "fail"
        elif self.validate_month(month_info) == False:
            return "fail"
        elif self.validate_cvc(cvc_info) == False:
            return "fail"
        else:
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

validation_result = Validate().validate_all()


# publish_event('paymentInfo', {'status': '{validation_result}', 'orderId': f"{order_id}"})
publish_event('fanout', [
    {
        "orderId": f"{order_id}",
        "paymentInfo": f"{validation_result}"
    }
])
publish_event()