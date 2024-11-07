import json
import os

class MerchantRepository:
    def __init__(self, file_path: str = './data/merchants.json'):
        self.file_path = file_path
        # Ensure the JSON file exists
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as file:
                json.dump({}, file)  # Start with an empty dictionary

    def save_merchant(self, name: str, ssn: str, email: str, phone_number: str, allows_discount: bool) -> int:
        # Load existing buyers
        with open(self.file_path, 'r+') as file:
            merchants = json.load(file)
            
            # Find the next available integer ID
            next_id = len(merchants) + 1  # Just use the next available number
            
            merchant_data = {
                "name": name,
                "ssn": ssn,
                "email": email,
                "phoneNumber": phone_number,
                "allowsDiscount": allows_discount
            }

            # Save the new buyer with the next available ID
            merchants[next_id] = merchant_data  # Use an integer ID
            file.seek(0)
            json.dump(merchants, file, indent=4)  # Save back to file

        return next_id  # Return the new buyer's ID

    def get_merchant(self, merchant_id: int) -> dict:
        # Load the buyers and return the one matching the ID, or None if not found
        with open(self.file_path, 'r') as file:
            merchants = json.load(file)
            return merchants.get(merchant_id)  # Directly access by integer ID
