import json
import os
from models import CreditCard

class OrderRepository:
    def __init__(self, file_path: str = './data/orders.json'):
        self.file_path = file_path
        # Ensure the JSON file exists
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as file:
                json.dump({}, file)  # Start with an empty dictionary

    def save_order(self, productId: int, merchantId: str, buyerId: float, creditCard: CreditCard,  discount: float) -> int:
        # Load existing products
        with open(self.file_path, 'r+') as file:
            orders = json.load(file)
            
            # Find the next available integer ID
            next_id = len(orders) + 1  # Just use the next available number
            
            # Create the product
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
                "discount": discount  # Initially no products are reserved
            }

            # Save the new product with the next available ID
            orders[next_id] = order_data
            file.seek(0)
            json.dump(orders, file, indent=4)  # Save back to file

        return next_id  # Return the new product's ID

    def get_order(self, order_id: int) -> dict:
        # Load the products and return the one matching the ID, or None if not found
        with open(self.file_path, 'r') as file:
            orders = json.load(file)
            return orders.get(str(order_id))  # Directly access by integer ID
