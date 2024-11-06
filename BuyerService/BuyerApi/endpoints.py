
from fastapi import APIRouter, Depends, HTTPException
from dependency_injector.wiring import inject, Provide
from BuyerApi.container import Container
from BuyerApi.buyer_repository import BuyerRepository
from BuyerApi.buyer_sender import BuyerSender
from BuyerApi.models.buyer_model import Buyer
from pydantic import BaseModel

router = APIRouter()

# POST endpoint to create a new buyer
@router.post("/buyers", status_code=201)
@inject
async def create_buyer(
    buyer: Buyer,  # Receive the Buyer object (Pydantic model)
    buyer_repository: BuyerRepository = Depends(Provide[Container.buyer_repository_provider]),
    buyer_sender: BuyerSender = Depends(Provide[Container.buyer_sender_provider]),
):
    # Convert Buyer model to dictionary and save it
    buyer_data = buyer.dict()  # Convert the Pydantic model to a dictionary
    buyer_id = buyer_repository.save_buyer(buyer_data)  # Save the buyer and get the ID
    
    # Send a message about the new buyer
    buyer_sender.send_message(buyer_data)
    
    # Return the buyer ID as JSON response
    return {"id": buyer_id}

# GET endpoint to retrieve a buyer by ID
@router.get("/buyers/{id}", response_model=Buyer)  # Specify response_model to automatically serialize
@inject
async def get_buyer(
    id: int,
    buyer_repository: BuyerRepository = Depends(Provide[Container.buyer_repository_provider]),
):
    # Retrieve the buyer by ID
    buyer = buyer_repository.get_buyer_by_id(id)
    if buyer is None:
        raise HTTPException(status_code=404, detail="Buyer not found")
    
    # Return the buyer (Pydantic model) directly, FastAPI will serialize it to JSON
    return buyer