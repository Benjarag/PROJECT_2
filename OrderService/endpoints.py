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
async def save_orders(order: OrderModel,
                        order_sender: OrderSender = Depends(
                            Provide[Container.order_sender_provider]),
                        order_repository: OrderRepository = Depends(
                            Provide[Container.order_repository_provider])):

    # TODO: save order and send order event
    order_id = order_repository.save_order(order.order)  # Save the order to the repository
    order_sender.send_order(order.order)  # Send order event through the order sender
    return {"id": order_id}
