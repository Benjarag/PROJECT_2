from fastapi import APIRouter, Depends, HTTPException
from dependency_injector.wiring import inject, Provide
from models.order_model import OrderModel
from container import Container
from order_repository import OrderRepository
from order_sender import OrderSender

router = APIRouter()

@router.get('/orders/{id}', status_code=200)
@inject
async def get_order(
    id: int, 
    order_repository: OrderRepository = Depends(Provide[Container.order_repository_provider])
):
    order = order_repository.get_order(id)
    
    # Only raise exception if the order is not found
    if order == "Order not found":
        raise HTTPException(status_code=404, detail="Order does not exist")

    # Return the order if found
    return order


@router.post('/orders', status_code=201)
@inject
async def create_order(
    order: OrderModel,
    order_repository: OrderRepository = Depends(Provide[Container.order_repository_provider]),
    order_sender: OrderSender = Depends(Provide[Container.order_sender_provider])
):
    # Validate the order before saving
    validation_result = order_repository.validate_order(order.dict())
    if validation_result is not None:
        raise HTTPException(status_code=400, detail=validation_result)

    # Save the order and get the generated order ID
    order_id = order_repository.save_order(order.dict())
    
    # Send order creation event
    order_sender.send_order(order.dict())

    return {"id": order_id}
