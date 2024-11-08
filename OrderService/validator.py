from fastapi import HTTPException
from models import OrderRequest
import httpx

MERCHANT_URL = "http://merchant-service:8001/merchants/"
BUYER_URL = "http://buyer-service:8002/buyers/"
PRODUCTS_URL = "http://inventory-service:8003/products/"

async def validate_order(order: OrderRequest) -> None:
    """Validate the order details by making GET requests to MerchantService, BuyerService, and InventoryService."""
    
    async with httpx.AsyncClient() as client:
        # Validate merchant
        merchant_response = await client.get(MERCHANT_URL + str(order.merchantId))
        if merchant_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Merchant does not exist")
        merchant = merchant_response.json()

        # Validate buyer
        buyer_response = await client.get(BUYER_URL + str(order.buyerId))
        if buyer_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Buyer does not exist")
        buyer = buyer_response.json()

        # Validate product
        product_response = await client.get(PRODUCTS_URL + str(order.productId))
        if product_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Product does not exist")
        product = product_response.json()

        # Check if product is sold out
        if product["quantity"] <= 0:
            raise HTTPException(status_code=400, detail="Product is sold out")

        # Validate product ownership
        if product["merchantId"] != order.merchantId:
            raise HTTPException(status_code=400, detail="Product does not belong to merchant")

        # Check discount permission
        if not merchant["allowsDiscount"] and order.discount != 0:
            raise HTTPException(status_code=400, detail="Merchant does not allow discount")

        # Reserve product
        product_reserve_response = await client.put(PRODUCTS_URL + str(order.productId))
        if product_reserve_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Product reservation failed")
