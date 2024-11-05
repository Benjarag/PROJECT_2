import json
from typing import List, Optional

class BuyerRepository:
    def __init__(self, file_path: str = '/app/data/buyers.json'):
        self.file_path = file_path

    def read_buyers(self) -> List[dict]:
        """Read buyers from the JSON file."""
        try:
            with open(self.file_path) as f:
                data = json.load(f)
                return data["buyers"]
        except FileNotFoundError:
            return []

    def get_buyer_by_id(self, buyer_id: int) -> Optional[dict]:
        """Get a buyer by ID."""
        buyers = self.read_buyers()
        for buyer in buyers:
            if buyer["id"] == buyer_id:
                return buyer
        return None

    def save_buyer(self, buyer: dict) -> int:
        """Save a new buyer to the JSON file and return the new buyer ID."""
        buyers = self.read_buyers()
        new_id = max(buyer["id"] for buyer in buyers) + 1 if buyers else 1
        buyer["id"] = new_id
        buyers.append(buyer)
        
        # Write back to the JSON file
        with open(self.file_path, 'w') as f:
            json.dump({"buyers": buyers}, f)
        
        return new_id
