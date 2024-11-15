from fastapi import APIRouter, HTTPException
import httpx
from utils import calculate_total_price, mask_card_number
from order_repository import OrderRepository
from validator import validate_order
from models import OrderRequest
from events import EventManager

router = APIRouter()
order_repo = OrderRepository(file_path='./data/orders.json')

event_manager = EventManager()

MERCHANT_URL = "http://merchant-service:8001/merchants/"
BUYER_URL = "http://buyer-service:8002/buyers/"
PRODUCTS_URL = "http://inventory-service:8003/products/"

@router.post("/orders", status_code=201)
async def create_order(order: OrderRequest):
    await validate_order(order)
    order_id = order_repo.save_order(
        productId=order.productId,
        merchantId=order.merchantId,
        buyerId=order.buyerId,
        creditCard=order.creditCard,
        discount=order.discount
    )
    order = order_repo.get_order(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order does not exist")
    
    async with httpx.AsyncClient() as client:
        product_response = await client.get(PRODUCTS_URL + str(order["productId"]))
        if product_response.status_code != 200:
            raise HTTPException(status_code=404, detail="Product not found")
        product = product_response.json()

        merchant_response = await client.get(MERCHANT_URL + str(order["merchantId"]))
        if merchant_response.status_code != 200:
            raise HTTPException(status_code=404, detail="Merchant not found")
        merchant = merchant_response.json()

        buyer_response = await client.get(BUYER_URL + str(order["buyerId"]))
        if buyer_response.status_code != 200:
            raise HTTPException(status_code=404, detail="Buyer not found")
        buyer = buyer_response.json()

    event_data = {
        "order_id": order_id,  
        "buyer_mail": buyer["email"],
        "merchant_mail": merchant["email"],
        "product_price": product["price"],
        "product_name": product["productName"],
        "card_number": order["creditCard"]["cardNumber"],
        "year_expiration": order["creditCard"]["expirationYear"],
        "month_expiration": order["creditCard"]["expirationMonth"],
        "cvc": order["creditCard"]["cvc"]
    }

    event_manager.publish_event(event_data)

    return {"order_id": order_id}
    

@router.get("/orders/{id}", status_code=200)
async def get_order(id: str):
    order = order_repo.get_order(id)

    if order is None:
        raise HTTPException(status_code=404, detail="Order does not exist")
    
    product = order["productId"].json()

    if product.get("price") is None:
        raise HTTPException(status_code=400, detail="Price not found")

    total_price = calculate_total_price(product["price"], order["discount"])

    response_data = {
        "productId": order["productId"],  
        "merchantId": order["merchantId"],
        "buyerId": order["buyerId"],
        "cardNumber": mask_card_number(order["creditCard"]["cardNumber"]),
        "totalPrice": total_price
    }
    
    return response_data



    

