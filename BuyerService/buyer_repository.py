import json
import os

class BuyerRepository:
    def __init__(self, file_path: str = './data/buyers.json'):
        self.file_path = file_path
        # Ensure the JSON file exists
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as file:
                json.dump({}, file)  # Start with an empty dictionary

    def save_buyer(self, name: str, ssn: str, email: str, phone_number: str) -> int:
        # Load existing buyers
        with open(self.file_path, 'r+') as file:
            buyers = json.load(file)
            
            # Find the next available integer ID
            next_id = len(buyers) + 1  # Just use the next available number
            
            buyer_data = {
                "name": name,
                "ssn": ssn,
                "email": email,
                "phoneNumber": phone_number
            }

            # Save the new buyer with the next available ID
            buyers[next_id] = buyer_data  # Use an integer ID
            file.seek(0)
            json.dump(buyers, file, indent=4)  # Save back to file

        return next_id  # Return the new buyer's ID

    def get_buyer(self, buyer_id: int) -> dict:
        # Load the buyers and return the one matching the ID, or None if not found
        with open(self.file_path, 'r') as file:
            buyers = json.load(file)
            return buyers.get(buyer_id)  # Directly access by integer ID
