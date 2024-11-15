import json
import os

class InventoryRepository:
    def __init__(self, file_path: str = './data/inventory.json'):
        self.file_path = file_path
        # Ensure the JSON file exists
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as file:
                json.dump({}, file)  

    def save_product(self, merchant_id: int, product_name: str, price: float, quantity: int) -> int:
        with open(self.file_path, 'r+') as file:
            products = json.load(file)
            
            next_id = len(products) + 1  
            
            product_data = {
                "merchantId": merchant_id,
                "productName": product_name,
                "price": float(price),  
                "quantity": quantity,
                "reserved": 0
            }

            products[next_id] = product_data
            file.seek(0)
            json.dump(products, file, indent=4)

        return next_id 


    def get_product(self, product_id: int) -> dict:
        with open(self.file_path, 'r') as file:
            products = json.load(file)
            return products.get(product_id) 

    def update_product(self, product_id: int) -> int:
       with open(self.file_path, 'r+') as file:
           products = json.load(file)
           products[product_id]["quantity"] -= 1
           products[product_id]["reserved"] += 1
           file.seek(0)
           json.dump(products, file, indent=4)
           file.truncate()
       return product_id, products.get(product_id)
    
 
    def update_product_on_payment(self, product_id: int, payment_success: bool) -> int:
        with open(self.file_path, 'r+') as file:
            products = json.load(file)

            if product_id not in products:
                raise ValueError(f"Product with ID {product_id} not found")

            product = products[product_id]

            if payment_success:
                if product["reserved"] > 0:
                    product["reserved"] -= 1
                else:
                    raise ValueError("No reserved units to decrease")
            else:
                if product["reserved"] > 0:
                    product["reserved"] -= 1
                    product["quantity"] += 1
                else:
                    raise ValueError("No reserved units to revert")

            file.seek(0)
            json.dump(products, file, indent=4)
            file.truncate()

        return product_id, product