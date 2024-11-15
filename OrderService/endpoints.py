from fastapi import APIRouter, HTTPException
import httpx
from utils import calculate_total_price, mask_card_number
from order_repository import OrderStorage
from validator import validate_order_data
from models import OrderInput
from events import NotificationManager

api_router = APIRouter()
order_storage = OrderStorage(file_path='./data/orders.json')
notification_manager = NotificationManager()

SELLER_URL = "http://merchant-service:8001/merchants/"
CUSTOMER_URL = "http://buyer-service:8002/buyers/"
ITEMS_URL = "http://inventory-service:8003/products/"

@api_router.post("/orders", status_code=201)
async def initiate_order(order_data: OrderInput):
    await validate_order_data(order_data)
    transaction_id = order_storage.save_order(
        productId=order_data.productId,
        merchantId=order_data.merchantId,
        buyerId=order_data.buyerId,
        creditCard=order_data.creditCard,
        discount=order_data.discount
    )
    saved_order = order_storage.get_order(transaction_id)
    if saved_order is None:
        raise HTTPException(status_code=404, detail="Order does not exist")
    
    async with httpx.AsyncClient() as async_client:
        item_response = await async_client.get(ITEMS_URL + str(saved_order["productId"]))
        if item_response.status_code != 200:
            raise HTTPException(status_code=404, detail="Product not found")
        item_details = item_response.json()

        seller_response = await async_client.get(SELLER_URL + str(saved_order["merchantId"]))
        if seller_response.status_code != 200:
            raise HTTPException(status_code=404, detail="Merchant not found")
        seller_details = seller_response.json()

        customer_response = await async_client.get(CUSTOMER_URL + str(saved_order["buyerId"]))
        if customer_response.status_code != 200:
            raise HTTPException(status_code=404, detail="Buyer not found")
        customer_details = customer_response.json()

    event_payload = {
        "order_id": transaction_id,
        "buyer_mail": customer_details["email"],
        "merchant_mail": seller_details["email"],
        "product_price": item_details["price"],
        "product_name": item_details["productName"],
        "card_number": saved_order["creditCard"]["cardNumber"],
        "year_expiration": saved_order["creditCard"]["expirationYear"],
        "month_expiration": saved_order["creditCard"]["expirationMonth"],
        "cvc": saved_order["creditCard"]["cvc"]
    }

    notification_manager.publish_event(event_payload)

    return {"order_id": transaction_id}
    

@api_router.get("/orders/{transaction_id}", status_code=200)
async def retrieve_order(transaction_id: str):
    retrieved_order = order_storage.get_order(transaction_id)

    if retrieved_order is None:
        raise HTTPException(status_code=404, detail="Order does not exist")
    
    item_data = retrieved_order["productId"].json()

    if item_data.get("price") is None:
        raise HTTPException(status_code=400, detail="Price not found")

    calculated_price = calculate_total_price(item_data["price"], retrieved_order["discount"])

    response



    

