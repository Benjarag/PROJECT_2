from fastapi import FastAPI, HTTPException, status
from typing import List
from merchant_repository import MerchantRepository
from models.merchant_model import Merchant

app = FastAPI()
merchant_repository = MerchantRepository()

@app.post("/merchants", response_model=int, status_code=status.HTTP_201_CREATED)
async def create_merchant(merchant: Merchant):
    """Create a new merchant."""
    merchant_id = merchant_repository.save_merchant(merchant.dict())
    return merchant_id

@app.get("/merchants/{id}", response_model=Merchant, status_code=status.HTTP_200_OK)
async def get_merchant(id: int):
    """Retrieve a merchant by ID."""
    merchant = merchant_repository.get_merchant(id)
    if not merchant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Merchant not found")
    return merchant

@app.get("/merchants", response_model=List[Merchant])
async def list_merchants():
    """List all merchants."""
    return merchant_repository.merchants()
