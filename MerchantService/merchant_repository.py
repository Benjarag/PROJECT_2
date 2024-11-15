import json
import os

class MerchantRepository:
    def __init__(self, file_path: str = './data/merchants.json'):
        self.file_path = file_path
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as file:
                json.dump({}, file) 

    def save_merchant(self, name: str, ssn: str, email: str, phone_number: str, allows_discount: bool) -> int:
        with open(self.file_path, 'r+') as file:
            merchants = json.load(file)
            
            next_id = len(merchants) + 1
            
            merchant_data = {
                "name": name,
                "ssn": ssn,
                "email": email,
                "phoneNumber": phone_number,
                "allowsDiscount": allows_discount
            }

            merchants[next_id] = merchant_data 
            file.seek(0)
            json.dump(merchants, file, indent=4) 

        return next_id 

    def get_merchant(self, merchant_id: int) -> dict:
        with open(self.file_path, 'r') as file:
            merchants = json.load(file)
            return merchants.get(merchant_id) 
