from pydantic import BaseModel


class OrderMail(BaseModel):
    order_id: int
    buyer_mail: str
    merchant_mail: str
    product_price: float
    product_name: str
    card_number: str
    year_expiration: int
    month_expiration: int
    cvc: int