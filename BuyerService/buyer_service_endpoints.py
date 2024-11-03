from fastapi import APIRouter, Depends, HTTPException
from dependency_injector.wiring import inject, Provide
from models.buyer_model import BuyerModel
from buyer_service_container import Container
from buyer_service import BuyerService
from buyer_repository import BuyerRepository

router = APIRouter()

@router.get('/buyers/{id}', status_code=200)
@inject
async def get_buyer(
    id: int, 
    buyer_service: BuyerRepository = Depends(Provide[Container.buyer_repository_provider])
):
    buyer = buyer_repository.get_buyer(id)
    
    # Only raise exception if the buyer is not found
    if buyer == "Buyer not found":
        raise HTTPException(status_code=404, detail="Buyer does not exist")

    # Return the buyer if found
    return buyer

@router.post('/buyers', status_code=201)
@inject
async def save_buyers(buyer: BuyerModel,
                        buyer_service: BuyerService = Depends(
                            Provide[Container.buyer_service_provider]),
                        buyer_repository: BuyerRepository = Depends(
                            Provide[Container.buyer_repository_provider])):
    # Save the buyer to the repository
    buyer_id = buyer_repository.save_buyer(buyer.buyer)
    buyer_sender.send_buyer(buyer.buyer)  # Send buyer event through the buyer sender
    return {"id": buyer_id}