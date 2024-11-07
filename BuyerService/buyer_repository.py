import json
import os
import uuid

class BuyerRepository:
    def __init__(self, file_path: str = './data/buyers.json'):
        self.file_path = file_path
        # Ensure the directory exists
        #os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        # Ensure the JSON file exists
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as file:
                json.dump({}, file)  # Start with an empty JSON dictionary

    def save_buyer(self, name: str, ssn: str, email: str, phone_number: str) -> str:
        # Create a unique ID for the new buyer
        buyer_id = str(uuid.uuid4())
        buyer_data = {
            "name": name,
            "ssn": ssn,
            "email": email,
            "phoneNumber": phone_number
        }

        # Load existing buyers, add the new buyer, then save back to the file
        with open(self.file_path, 'r+') as file:
            buyers = json.load(file)
            buyers[buyer_id] = buyer_data
            file.seek(0)
            json.dump(buyers, file, indent=4)

        return buyer_id  # Return the ID of the newly created buyer

    def get_buyer(self, buyer_id: str) -> dict:
        # Load the buyers and return the one matching the ID, or None if not found
        with open(self.file_path, 'r') as file:
            buyers = json.load(file)
            return buyers.get(buyer_id)
