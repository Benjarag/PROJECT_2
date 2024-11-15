import json
from pathlib import Path

DB_PATH = Path("app/database/payments.json")

class PaymentRepository:
    def __init__(self):
        self.db_path = DB_PATH
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.db_path.exists():
            self.db_path.write_text(json.dumps([]))

    def save_payment_result(self, order_id: str, result: str):
        data = self.load_data()
        data.append({"order_id": order_id, "result": result})
        self.db_path.write_text(json.dumps(data, indent=4))

    def load_data(self):
        with self.db_path.open("r") as f:
            return json.load(f)
