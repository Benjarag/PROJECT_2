from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Optional
from utils import mask_card_number

app = FastAPI()

# Mock database and validation functions
orders_db = {}
merchants = {123: {"allows_discount": True, "products": {123: {"price": 100, "stock": 5}}}}
buyers = {123: {}}

# Request body model for creating an order
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

@app.post("/orders", status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderRequest):
    # Validate merchant
    if order.merchantId not in merchants:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Merchant does not exist")
    
    # Validate buyer
    if order.buyerId not in buyers:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Buyer does not exist")
    
    # Validate product
    merchant = merchants[order.merchantId]
    if order.productId not in merchant["products"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product does not exist")
    
    product = merchant["products"][order.productId]
    
    # Check if product is sold out
    if product["stock"] <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product is sold out")
    
    # Validate product ownership
    if order.merchantId not in [m_id for m_id in merchants if order.productId in merchants[m_id]["products"]]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product does not belong to merchant")
    
    # Check discount permission
    if not merchant["allows_discount"] and order.discount != 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Merchant does not allow discount")
    
    # Reserve product and save order to database
    product["stock"] -= 1
    order_id = len(orders_db) + 1
    orders_db[order_id] = {
        "productId": order.productId,
        "merchantId": order.merchantId,
        "buyerId": order.buyerId,
        "cardNumber": order.creditCard.cardNumber,
        "discount": order.discount,
        "totalPrice": product["price"] * (1 - order.discount)
    }

    # Send event to RabbitMQ (pseudo-code for illustration)
    # publish_message("order_created", str(orders_db[order_id]))

    return {"message": "Order created successfully", "orderId": order_id}

@app.get("/orders/{id}", response_model=OrderResponse)
async def get_order(id: int):
    # Retrieve order
    order = orders_db.get(id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order does not exist")

    # Mask the credit card number for the response
    masked_card_number = mask_card_number(order["cardNumber"])
    
    response = OrderResponse(
        productId=order["productId"],
        merchantId=order["merchantId"],
        buyerId=order["buyerId"],
        cardNumber=masked_card_number,
        totalPrice=order["totalPrice"]
    )
    
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
