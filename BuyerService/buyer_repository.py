import json
import os

class BuyerRepository:
    def __init__(self, file_path: str = '/data/buyers.json'):
        self.file_path = file_path
        self._current_id = self._get_max_id()
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as file:
                json.dump({}, file)  # Start with an empty JSON dictionary

    def _get_max_id(self) -> int:
        # Load existing buyers and determine the next ID
        try:
            with open(self.file_path, 'r') as file:
                buyers = json.load(file)
                # Return 1 if buyers dictionary is empty, else max ID + 1
                return max(int(buyer_id) for buyer_id in buyers.keys()) if buyers else 1
        except FileNotFoundError:
            return 1  # Start with ID 1 if file does not exist

    def save_buyer(self, name: str, ssn: str, email: str, phone_number: str) -> int:
        # Get the next buyer ID
        buyer_id = self._current_id
        self._current_id += 1
        buyer_data = {
            "id": buyer_id,
            "name": name,
            "ssn": ssn,
            "email": email,
            "phoneNumber": phone_number
        }

        # Load existing buyers, add the new buyer, then save back to the file
        with open(self.file_path, 'r+') as file:
            buyers = json.load(file)
            buyers[str(buyer_id)] = buyer_data
            file.seek(0)
            json.dump(buyers, file, indent=4)

        return buyer_id  # Return the ID of the newly created buyer

    def get_buyer(self, buyer_id: int) -> dict:
        # Load the buyers and return the one matching the ID, or None if not found
        with open(self.file_path, 'r') as file:
            buyers = json.load(file)
            return buyers.get(str(buyer_id))
