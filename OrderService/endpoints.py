from fastapi import APIRouter, HTTPException
from OrderService.order_event_sender import publish_event
from utils import calculate_total_price, mask_card_number
from order_repository import OrderRepository
from validator import validate_order
from models import OrderRequest
from order_event_sender import publish_event

# Create FastAPI app instance
router = APIRouter()
# Assuming ORDER_SERVICE_URL is a dictionary that stores orders
order_repo = OrderRepository(file_path='./data/orders.json')

@router.post("/orders", status_code=201)
async def create_order(order: OrderRequest):
    # Validate merchant and buyer
    await validate_order(order)
    order_id = order_repo.save_order(
        productId=order.productId,
        merchantId=order.merchantId,
        buyerId=order.buyerId,
        creditCard=order.creditCard,
        discount=order.discount
    )
    # send an event that the order has been created
    order = order_repo.get_order(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order does not exist")

    product = order["productId"].json()
    merchant = order["merchantId"].json()
    buyer = order["buyerId"].json()

    event_data = {
        "order_id": order_id,  # Correct access to order data
        "buyer_mail": buyer["email"],
        "merchant_mail": merchant["email"],
        "product_price": product["price"],
        "prduct_name": product["productName"],
        "year_expiration": order["creditCard"]["expirationYear"],
        "month_expiration": order["creditCard"]["expirationMonth"],
        "cvc": order["creditCard"]["cvc"]
    }

    publish_event(event_data)

    return {"order_id": order_id}
    
# Assuming the InventoryService is running at this base URL

@router.get("/orders/{id}", status_code=200)
async def get_order(id: str):
    # Retrieve order from the order repository
    order = order_repo.get_order(id)

    if order is None:
        raise HTTPException(status_code=404, detail="Order does not exist")
    
    product = order["productId"].json()

    # Check if the product price exists
    if product.get("price") is None:
        raise HTTPException(status_code=400, detail="Price not found")

    # Calculate the total price with the discount
    total_price = calculate_total_price(product["price"], order["discount"])

    # Prepare the response data
    response_data = {
        "productId": order["productId"],  # Correct access to order data
        "merchantId": order["merchantId"],
        "buyerId": order["buyerId"],
        "cardNumber": mask_card_number(order["creditCard"]["cardNumber"]),
        "totalPrice": total_price
    }
    
    return response_data



    

