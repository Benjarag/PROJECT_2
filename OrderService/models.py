from pydantic import BaseModel


class CreditCard(BaseModel):
    cardNumber: str
    expirationMonth: int
    expirationYear: int
    cvc: int

class OrderRequest(BaseModel):
    productId: int
    merchantId: int
    buyerId: int
    creditCard: CreditCard
    discount: float

# Response model for GET /orders/{id}
class OrderResponse(BaseModel):
    productId: int
    merchantId: int
    buyerId: int
    cardNumber: str
    totalPrice: float