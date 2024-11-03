import json
import os

from OrderService.utils.masking import mask_credit_card

class OrderRepository:
    def __init__(self, file_path):
        self.file_path = file_path

    def save_order(self, order_data) -> int:
        # Save order to persistent storage and return the generated ID
        order_id = self._get_next_id()

        # Include the ID in the order data
        order_data['id'] = order_id

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
            return "No orders found."

        for order in orders:
            if order['id'] == order_id:
                # Perform validation checks
                merchant_id = order.get('merchantId')
                buyer_id = order.get('buyerId')
                product_id = order.get('productId')
                discount = order.get('discount', 0)

                if not self.merchant_exists(merchant_id):
                    return "Merchant does not exist"
                if not self.buyer_exists(buyer_id):
                    return "Buyer does not exist"
                if not self.product_exists(product_id):
                    return "Product does not exist"
                if self.is_product_sold_out(product_id):
                    return "Product is sold out"
                if not self.product_belongs_to_merchant(product_id, merchant_id):
                    return "Product does not belong to merchant"
                if not self.merchant_allows_discount(merchant_id, discount):
                    return "Merchant does not allow discount"

                # If all checks pass, mask card number and calculate total price
                order['cardNumber'] = mask_credit_card(order['creditCard']['cardNumber'])
                product_price = self.get_product_price(order['productId'])  # Implement as needed
                order['totalPrice'] = product_price * (1 - discount)

                # Return the order in the specified format
                return {
                    "productId": order['productId'],
                    "merchantId": order['merchantId'],
                    "buyerId": order['buyerId'],
                    "cardNumber": order['cardNumber'],
                    "totalPrice": order['totalPrice']
                }

        return "Order not found"

    # Example validation methods:
    def merchant_exists(self, merchant_id):
        # Implement the logic to check if the merchant exists
        return True  # Replace with actual validation

    def buyer_exists(self, buyer_id):
        # Implement the logic to check if the buyer exists
        return True  # Replace with actual validation

    def product_exists(self, product_id):
        # Implement the logic to check if the product exists
        return True  # Replace with actual validation

    def is_product_sold_out(self, product_id):
        # Implement the logic to check if the product is sold out
        return False  # Replace with actual validation

    def product_belongs_to_merchant(self, product_id, merchant_id):
        # Implement the logic to check if the product belongs to the merchant
        return True  # Replace with actual validation

    def merchant_allows_discount(self, merchant_id, discount):
        # Implement the logic to check if the merchant allows discounts
        return discount == 0  # Replace with actual validation