from fastapi import APIRouter, Depends, HTTPException
from dependency_injector.wiring import inject, Provide
from container import Container
from buyer_repository import BuyerRepository
from buyer_sender import BuyerSender
from models.buyer_model import Buyer

router = APIRouter()

@router.post("/buyers", status_code=201)
@inject
async def create_buyer(
    buyer: Buyer,
    buyer_repository: BuyerRepository = Depends(Provide[Container.buyer_repository_provider]),
    buyer_sender: BuyerSender = Depends(Provide[Container.buyer_sender_provider]),
):
    # Save the buyer to the repository and get the buyer ID
    buyer_data = buyer.dict()  # Convert the model to a dictionary
    buyer_id = buyer_repository.save_buyer(buyer_data)
    
    # Send a message about the new buyer
    buyer_sender.send_message(buyer_data)
    
    return {"id": buyer_id}

@router.get("/buyers/{id}", status_code=200)
@inject
async def get_buyer(
    id: int,
    buyer_repository: BuyerRepository = Depends(Provide[Container.buyer_repository_provider]),
):
    # Retrieve the buyer by ID
    buyer = buyer_repository.get_buyer_by_id(id)
    if buyer is None:
        raise HTTPException(status_code=404, detail="Buyer not found")
    return buyer
