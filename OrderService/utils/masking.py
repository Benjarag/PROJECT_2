def mask_credit_card(credit_card: str) -> str:
    return f"{'****-****-****-' + credit_card[-4:]}"  # Masking logic
