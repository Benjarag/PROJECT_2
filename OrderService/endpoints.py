from fastapi import FastAPI, HTTPException, status
import httpx
from order_repo import generate_order_id, read_orders, write_orders
from validator import validate_order
from models import OrderRequest, OrderResponse
from utils import mask_card_number

# Create FastAPI app instance
app = FastAPI()

# Assuming ORDER_SERVICE_URL is a dictionary that stores orders
ORDER_DATABASE = "OrderService\OrderDatabase.json"  # Define it if not already defined

# update the OrderService json, with get from inventory buyer and merchant 


@app.post("/orders", status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderRequest):
    try:
        # Validate merchant and buyer
        await validate_order(order)

        # Retrieve product info from the merchant service
        async with httpx.AsyncClient() as client:
            merchant_response = await client.get(f"http://merchantservice:8001/merchants/{order.merchantId}")
            merchant_response.raise_for_status()  # Raise an exception for HTTP errors
            merchant = merchant_response.json()

            # Ensure the product exists and retrieve it
            product = merchant["products"].get(order.productId)
            if not product:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product does not exist")

        # Check stock and reserve product
        if product["stock"] <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product is sold out")

        # Decrease stock
        product["stock"] -= 1

        # Read existing orders
        existing_orders = read_orders()
        
        # Generate new order ID
        order_id = generate_order_id(existing_orders)

        # Create new order entry
        new_order = {
            "id": order_id,
            "productId": order.productId,
            "merchantId": order.merchantId,
            "buyerId": order.buyerId,
            "cardNumber": order.creditCard.cardNumber,
            "discount": order.discount,
            "totalPrice": product["price"] * (1 - order.discount)
        }
        
        # Add new order to existing orders
        existing_orders.append(new_order)
        
        # Write updated orders back to JSON file
        write_orders(existing_orders)

        return {"message": "Order created successfully", "orderId": order_id}
    
    except httpx.HTTPStatusError as e:
        # Handle errors from the merchant service
        raise HTTPException(status_code=e.response.status_code, detail=f"Merchant service error: {e.response.text}")
    except Exception as e:
        # General error handling
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))



@app.get("/orders/{id}", response_model=OrderResponse)
async def get_order(id: int):
    # Retrieve order
    orders = read_orders()  # Use the previously defined read_orders function
    
    # Find the specific order by ID
    order = next((o for o in orders if o["id"] == id), None)
    
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

# Include the router in the FastAPI app

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
