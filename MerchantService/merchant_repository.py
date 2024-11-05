import json
import os

class MerchantRepository:
    def __init__(self):
        self.storage_file = 'MerchantService/MerchantDatabase.json'
        self.merchants = self._load_merchants()  # Load existing merchants on initialization

    def _load_merchants(self):
        """Load merchants from the JSON file."""
        if os.path.exists(self.storage_file):
            with open(self.storage_file, 'r') as file:
                return json.load(file)["merchants"]
        return []

    def save_merchant(self, merchant) -> int:
        """Save a new merchant to the database and return the new merchant ID."""
        merchant_id = self._get_next_id()
        merchant['id'] = merchant_id
        self.merchants.append(merchant)

        self._save_merchants()
        return merchant_id

    def _save_merchants(self):
        """Save the current list of merchants back to the JSON file."""
        with open(self.storage_file, 'w') as file:
            json.dump({"merchants": self.merchants}, file, indent=4)

    def _get_next_id(self) -> int:
        """Determine the next ID for a new merchant."""
        if self.merchants:
            return max(merchant["id"] for merchant in self.merchants) + 1
        return 1  # Start with ID 1 if there are no merchants

    def get_merchant(self, id: int):
        """Retrieve a merchant by ID."""
        for merchant in self.merchants:
            if merchant["id"] == id:
                return merchant
        return None  # Return None if merchant not found
