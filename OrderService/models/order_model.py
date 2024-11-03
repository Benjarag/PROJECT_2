from pydantic import BaseModel

class CreditCard(BaseModel):
    cardNumber: str
    expirationMonth: int
    expirationYear: int
    cvc: int

class OrderModel(BaseModel):
    productId: int
    merchantId: int
    buyerId: int
    creditCard: CreditCard
    discount: float = 0.0
