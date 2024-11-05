import json
ORDER_DATABASE_FILE = "OrderService/OrderDatabase.json"

def read_orders():
    try:
        with open(ORDER_DATABASE_FILE, 'r') as file:
            data = json.load(file)
            return data.get("orders", [])
    except FileNotFoundError:
        return []

def write_orders(orders):
    with open(ORDER_DATABASE_FILE, 'w') as file:
        json.dump({"orders": orders}, file, indent=4)

def generate_order_id(orders):
    return max(order['id'] for order in orders) + 1 if orders else 1
