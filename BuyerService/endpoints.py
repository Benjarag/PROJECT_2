from fastapi import APIRouter, Depends, HTTPException
from dependency_injector.wiring import inject, Provide
from models.buyer_model import BuyerModel
from container import Container
from buyer_repository import BuyerRepository
from buyer_sender import BuyerSender

router = APIRouter()

@router.get('/buyers/{id}', status_code=200)
@inject
async def get_buyer_by_id(
    id: int, 
    buyer_repository: BuyerRepository = Depends(Provide[Container.buyer_repository_provider])
):
    buyer = buyer_repository.get_buyer(id)
    
    # Only raise exception if the buyer is not found
    if buyer == "BUYER not found":
        raise HTTPException(status_code=404, detail="Buyer does not exist")

    # Return the Buyer if found
    return buyer


@router.post('/buyers', status_code=201)
@inject
async def create_buyer(buyer: BuyerModel,
                        buyer_sender: BuyerSender = Depends(
                            Provide[Container.buyer_sender_provider]),
                        buyer_repository: BuyerRepository = Depends(
                            Provide[Container.buyer_repository_provider])):

    # TODO: save buyer and send buyer event
    buyer_id = buyer_repository.create_buyer(buyer.buyer)  # Save the buyer to the repository
    buyer_sender.send_buyer(buyer.buyer)  # Send buyer event through the buyer sender
    return {"id": buyer_id}
