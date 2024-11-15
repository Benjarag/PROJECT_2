import json
import os
from models import CreditCard

class OrderRepository:
    def __init__(self, file_path: str = './data/orders.json'):
        self.file_path = file_path
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as file:
                json.dump({}, file)  

    def save_order(self, productId: int, merchantId: str, buyerId: float, creditCard: CreditCard,  discount: float) -> int:
        with open(self.file_path, 'r+') as file:
            orders = json.load(file)
            
            next_id = len(orders) + 1 
            
            order_data = {
                "productId": productId,
                "merchantId": merchantId,
                "buyerId": buyerId,
                "creditCard": {
                    "cardNumber": creditCard.cardNumber,
                    "expirationMonth": creditCard.expirationMonth,
                    "expirationYear": creditCard.expirationYear,
                    "cvc": creditCard.cvc
                },
                "discount": discount  
            }

            orders[next_id] = order_data
            file.seek(0)
            json.dump(orders, file, indent=4) 

        return next_id 

    def get_order(self, order_id: int) -> dict:
        with open(self.file_path, 'r') as file:
            orders = json.load(file)
            return orders.get(str(order_id))  
