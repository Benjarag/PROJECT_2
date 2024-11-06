import json
import os


class BuyerRepository:
    def __init__(self, file_path):
        self.file_path = file_path

    def create_buyer(self, buyer_data) -> int:
        """
        Creates and saves a buyer, assigning a unique ID to each new buyer.
        """
        buyer_id = self._get_next_id()
        buyer_data['id'] = buyer_id

        # Save buyer as JSON entry in file
        with open(self.file_path, 'a') as f:
            f.write(json.dumps(buyer_data) + '\n')
            print(f"Created buyer: {buyer_data}")  # Debugging print

        return buyer_id

    def _get_next_id(self) -> int:
        """
        Generate the next buyer ID by counting lines in the file.
        """
        try:
            with open(self.file_path, 'r') as f:
                return sum(1 for _ in f) + 1  # Next ID is the count + 1
        except FileNotFoundError:
            return 1  # Start with ID 1 if file does not exist

    def get_buyer(self, buyer_id) -> dict:
        """
        Retrieve a buyer by ID from the file.
        """
        try:
            with open(self.file_path, 'r') as f:
                buyers = [json.loads(line) for line in f.readlines()]
        except FileNotFoundError:
            return None  # No buyers file found

        for buyer in buyers:
            if buyer['id'] == buyer_id:
                return {
                    "name": buyer.get("name"),
                    "ssn": buyer.get("ssn"),
                    "email": buyer.get("email"),
                    "phoneNumber": buyer.get("phoneNumber"),
                }
        
        return None  # Buyer not found
