# merchant_repository.py
import json
from fastapi import HTTPException

class MerchantRepository:
    def __init__(self, file_path):
        self.file_path = file_path

    def save_merchant(self, merchant_data) -> int:
        merchant_id = self._get_next_id()
        merchant_data['id'] = merchant_id

        with open(self.file_path, 'a') as f:
            f.write(json.dumps(merchant_data) + '\n')

        return merchant_id

    def _get_next_id(self) -> int:
        try:
            with open(self.file_path, 'r') as f:
                count = sum(1 for _ in f)
                return count + 1
        except FileNotFoundError:
            return 1

    def get_merchant(self, merchant_id):
        try:
            with open(self.file_path, 'r') as f:
                merchants = [json.loads(line) for line in f.readlines()]
        except FileNotFoundError:
            return None

        for merchant in merchants:
            if merchant['id'] == merchant_id:
                return merchant

        return None
