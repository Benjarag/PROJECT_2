# endpoints.py
from fastapi import APIRouter, Depends, HTTPException
from models.merchant_model import MerchantModel
from merchant_repository import MerchantRepository
from dependency_injector.wiring import inject, Provide
from container import Container

router = APIRouter()

@router.post('/merchants', status_code=201)
@inject
async def create_merchant(
    merchant: MerchantModel,
    merchant_repository: MerchantRepository = Depends(Provide[Container.merchant_repository_provider])
):
    merchant_id = merchant_repository.save_merchant(merchant.dict())
    return {"id": merchant_id}

@router.get('/merchants/{id}', status_code=200)
@inject
async def get_merchant(
    id: int,
    merchant_repository: MerchantRepository = Depends(Provide[Container.merchant_repository_provider])
):
    merchant = merchant_repository.get_merchant(id)
    
    if merchant is None:
        raise HTTPException(status_code=404, detail="Merchant does not exist")

    return merchant
