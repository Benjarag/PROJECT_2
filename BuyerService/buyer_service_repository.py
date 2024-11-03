import json
import os

class BuyerRepository:
    def __init__(self, file_path):
        self.file_path = file_path

    def save_buyer(self, buyer_data) -> int:
        # Save buyer to persistent storage and return the generated ID
        buyer_id = self._get_next_id()

        # Include the ID in the buyer data
        buyer_data['id'] = buyer_id

        # Save the buyer in JSON format
        with open(self.file_path, 'a') as f:
            f.write(json.dumps(buyer_data) + '\n')
        
        return buyer_id
    
    def _get_next_id(self) -> int:
        # Retrieve the next buyer ID by counting existing buyers
        try:
            with open(self.file_path, 'r') as f:
                count = sum(1 for _ in f)
                return count + 1
        except FileNotFoundError:
            return 1
    
    def get_buyer(self, buyer_id):
        # Fetch and process buyer data as before
        try:
            with open(self.file_path, 'r') as f:
                buyers = [json.loads(line) for line in f.readlines()]
        except FileNotFoundError:
            return "No buyers found."
        
        for buyer in buyers:
            if buyer['id'] == buyer_id:
                return buyer
        
        return "Buyer not found"

