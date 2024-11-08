import json
import os

class InventoryRepository:
    def __init__(self, file_path: str = './data/inventory.json'):
        self.file_path = file_path
        # Ensure the JSON file exists
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as file:
                json.dump({}, file)  # Start with an empty dictionary

    def save_product(self, merchant_id: int, product_name: str, price: float, quantity: int) -> int:
    # Load existing products
        with open(self.file_path, 'r+') as file:
            products = json.load(file)
            
            # Find the next available integer ID
            next_id = len(products) + 1  # Just use the next available number
            
            # Create the product with price as a float
            product_data = {
                "merchantId": merchant_id,
                "productName": product_name,
                "price": float(price),  # Ensure price is a float
                "quantity": quantity,
                "reserved": 0
            }

            # Save the new product with the next available ID
            products[next_id] = product_data
            file.seek(0)
            json.dump(products, file, indent=4)  # Save back to file

        return next_id  # Return the new product's ID


    def get_product(self, product_id: int) -> dict:
        # Load the products and return the one matching the ID, or None if not found
        with open(self.file_path, 'r') as file:
            products = json.load(file)
            return products.get(product_id)  # Directly access by integer ID

    def update_product(self, product_id: int) -> int:
       # Load existing products
       with open(self.file_path, 'r+') as file:
           products = json.load(file)
           products[product_id]["quantity"] -= 1
           products[product_id]["reserved"] += 1
           file.seek(0)
           json.dump(products, file, indent=4)
           file.truncate()
       return product_id, products.get(product_id)