def luhn_algorithm(card_number: str) -> bool:
    digits = [int(d) for d in card_number][::-1]
    checksum = sum(digits[0::2]) + sum((2 * d) // 10 + (2 * d) % 10 for d in digits[1::2])
    return checksum % 10 == 0

def validate_card(card_number: str, month: int, year: int, cvc: str) -> bool:
    if not (luhn_algorithm(card_number)):
        return False
    if not (1 <= month <= 12):
        return False
    if not (1000 <= year <= 9999):
        return False
    if not (len(cvc) == 3 and cvc.isdigit()):
        return False
    return True
