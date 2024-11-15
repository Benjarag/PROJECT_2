import json
import os

class BuyerRepository:
    def __init__(self, file_path: str = './data/buyers.json'):
        self.file_path = file_path
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as file:
                json.dump({}, file)  

    def reserve_buyer(self, name: str, ssn: str, email: str, phone_number: str) -> int:
        with open(self.file_path, 'r+') as file:
            buyers = json.load(file)
            
            
            next_id = len(buyers) + 1 
            
            buyer_data = {
                "name": name,
                "ssn": ssn,
                "email": email,
                "phoneNumber": phone_number
            }

            buyers[next_id] = buyer_data  
            file.seek(0)
            json.dump(buyers, file, indent=4)  
        return next_id  

    def get_buyer(self, buyer_id: int) -> dict:
        with open(self.file_path, 'r') as file:
            buyers = json.load(file)
            return buyers.get(buyer_id)  
