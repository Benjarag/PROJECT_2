# Utility functions can be defined here
def mask_card_number(card_number: str) -> str:
    return "************" + card_number[-4:]
