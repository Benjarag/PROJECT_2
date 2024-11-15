from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from merchant_repository import MerchantRepository

router = APIRouter()
merchant_repo = MerchantRepository(file_path='./data/merchants.json')

class MerchantCreateRequest(BaseModel):
    name: str
    ssn: str
    email: str
    phoneNumber: str
    allowsDiscount: bool

@router.post("/merchants", status_code=201)
async def create_merchant(merchant: MerchantCreateRequest):
    merchant_id = merchant_repo.save_merchant(
        name=merchant.name,
        ssn=merchant.ssn,
        email=merchant.email,
        phone_number=merchant.phoneNumber,
        allows_discount=merchant.allowsDiscount
    )
    return {"merchant_id": merchant_id}

@router.get("/merchants/{id}", status_code=200)
async def get_buyer(id: str):
    merchant = merchant_repo.get_merchant(id)
    if merchant is None:
        raise HTTPException(status_code=404, detail="Merchant does not exist")
    return merchant
