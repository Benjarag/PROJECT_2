from fastapi import HTTPException
from models import OrderRequest
import httpx

MERCHANT_URL = "http://merchant-service:8001/merchants/"
BUYER_URL = "http://buyer-service:8002/buyers/"
PRODUCTS_URL = "http://inventory-service:8003/products/"

async def validate_order(order: OrderRequest) -> None:
    """Validate the order details by making GET requests to MerchantService, BuyerService, and InventoryService."""
    
    async with httpx.AsyncClient() as client:
        # Merchant validation
        merchant_response = await client.get(MERCHANT_URL + str(order.merchantId))
        if merchant_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Merchant does not exist")
        merchant = merchant_response.json()

        # Buyer validation
        buyer_response = await client.get(BUYER_URL + str(order.buyerId))
        if buyer_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Buyer does not exist")
        
        buyer = buyer_response.json()

        # Product validation
        product_response = await client.get(PRODUCTS_URL + str(order.productId))
        if product_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Product does not exist")
        product = product_response.json()

        if product["quantity"] <= 0:
            raise HTTPException(status_code=400, detail="Product has sold out")

        if product["merchantId"] != order.merchantId:
            raise HTTPException(status_code=400, detail="Product does not belong to merchant")

        if not merchant["allowsDiscount"] and order.discount != 0:
            raise HTTPException(status_code=400, detail="Merchant does not allow any discount")

        product_reserve_response = await client.put(PRODUCTS_URL + str(order.productId))
        if product_reserve_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Product reservation failed")
