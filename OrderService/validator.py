from typing import Dict
from fastapi import HTTPException, status
from models import OrderRequest
import httpx

MERCHANT_URL = "http://localhost:8001/merchants/"
BUYER_URL = "http://localhost:8002/buyer/"

async def validate_order(order: OrderRequest) -> None:
    """Validate the order details by making GET requests to MerchantService and BuyerService."""
    
    # Validate merchant
    async with httpx.AsyncClient() as client:
        merchant_response = await client.get(MERCHANT_URL + str(order.merchantId))  # Ensure merchantId is a string
        if merchant_response.status_code != 200:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Merchant does not exist")
    
    merchant = merchant_response.json()

    # Validate buyer
    buyer_response = await client.get(BUYER_URL + str(order.buyerId))  # Ensure buyerId is a string
    if buyer_response.status_code != 200:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Buyer does not exist")

    buyer = buyer_response.json()

    # Validate product
    if order.productId not in merchant.get("products", {}):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product does not exist")

    product = merchant["products"][order.productId]

    # Check if product is sold out
    if product["stock"] <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product is sold out")

    # Validate product ownership
    if order.merchantId not in [m_id for m_id in merchant["products"] if order.productId in merchant["products"][m_id]]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product does not belong to merchant")

    # Check discount permission
    if not merchant["allows_discount"] and order.discount != 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Merchant does not allow discount")
    
    # async with httpx.AsyncClient() as client:
    #     merchant_response = await client.get(MERCHANT_URL + str(order.merchantId))
    #     merchant = merchant_response.json()
        
    #     # Ensure the product exists and retrieve it
    #     product = merchant["products"].get(order.productId)
    #     if not product:
    #         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product does not exist")
    

    # No need to return anything; function completes successfully if validations pass.
