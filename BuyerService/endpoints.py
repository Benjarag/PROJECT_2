from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from buyer_repository import BuyerRepository

router = APIRouter()
buyer_repo = BuyerRepository(file_path='./data/buyers.json')

# Request model for buyer data
class BuyerCreateRequest(BaseModel):
    name: str
    ssn: str
    email: str
    phoneNumber: str

# Endpoint to create a buyer
@router.post("/buyers", status_code=201)
async def create_buyer(buyer: BuyerCreateRequest):
    buyer_id = buyer_repo.save_buyer(
        name=buyer.name,
        ssn=buyer.ssn,
        email=buyer.email,
        phone_number=buyer.phoneNumber
    )
    return {"buyer_id": buyer_id}

# Endpoint to retrieve a buyer by ID
@router.get("/buyers/{id}", status_code=200)
async def get_buyer(id: str):
    buyer = buyer_repo.get_buyer(id)
    if buyer is None:
        raise HTTPException(status_code=404, detail="Buyer does not exist")
    return buyer
