import json
from fastapi import HTTPException
from OrderService.utils.masking import mask_credit_card

class OrderRepository:
    def __init__(self, file_path):
        self.file_path = file_path

    def save_order(self, order_data) -> int:
        # Save order to persistent storage and return the generated ID
        order_id = self._get_next_id()
        order_data['id'] = order_id  # include the id in the order data

        # Save the order in JSON format
        with open(self.file_path, 'a') as f:
            f.write(json.dumps(order_data) + '\n')  # Write each order as a JSON line
            print(f"Saved order: {order_data}")  # Debugging print

        return order_id

    def _get_next_id(self) -> int:
        # Retrieve the next order ID by counting existing orders
        try:
            with open(self.file_path, 'r') as f:
                count = sum(1 for _ in f)  # Count lines to determine next ID
                print(f"Current order count: {count}")  # Debugging print
                return count + 1
        except FileNotFoundError:
            return 1  # Start with ID 1 if the file does not exist

    def get_order(self, order_id):
        # Fetch and process order data as before
        try:
            with open(self.file_path, 'r') as f:
                orders = [json.loads(line) for line in f.readlines()]
        except FileNotFoundError:
            return "Order not found"

        for order in orders:
            if order['id'] == order_id:
                # Perform validation checks
                order['cardNumber'] = mask_credit_card(order['creditCard']['cardNumber'])
                product_price = self.get_product_price(order['productId'])  # Implement as needed
                order['totalPrice'] = product_price * (1 - order.get('discount', 0))

                return {
                    "productId": order['productId'],
                    "merchantId": order['merchantId'],
                    "buyerId": order['buyerId'],
                    "cardNumber": order['cardNumber'],
                    "totalPrice": order['totalPrice']
                }

        return "Order not found"

    def validate_order(self, order):
        if not self.merchant_exists(order['merchantId']):
            raise HTTPException(status_code=400, detail="Merchant does not exist")
        
        if not self.buyer_exists(order['buyerId']):
            raise HTTPException(status_code=400, detail="Buyer does not exist")
        
        if not self.product_exists(order['productId']):
            raise HTTPException(status_code=400, detail="Product does not exist")
        
        if self.is_product_sold_out(order['productId']):
            raise HTTPException(status_code=400, detail="Product is sold out")
        
        if not self.product_belongs_to_merchant(order['productId'], order['merchantId']):
            raise HTTPException(status_code=400, detail="Product does not belong to merchant")
        
        if not self.merchant_allows_discount(order['discount']):
            raise HTTPException(status_code=400, detail="Merchant does not allow discount")

    # Example validation methods:
    def merchant_exists(self, merchant_id):
        # how do I check this?!
        return merchant_id in self.merchant_data_source
    
    def buyer_exists(self, buyer_id):
        # how do I check this?!
        return True  # Replace with actual validation

    def product_exists(self, product_id):
        # how do I check this?!
        return True  # Replace with actual validation

    def is_product_sold_out(self, product_id):
        # how do I check this?!
        return False  # Replace with actual validation

    def product_belongs_to_merchant(self, product_id, merchant_id):
        # how do I check this?!
        return True  # Replace with actual validation

    def merchant_allows_discount(self, discount):
        return True