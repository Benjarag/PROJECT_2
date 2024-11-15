def mask_card_number(card_number: str) -> str:
    return "************" + card_number[-4:]

def calculate_total_price(price: float, discount: float) -> float:
    return round(price * (1 - discount), 2)