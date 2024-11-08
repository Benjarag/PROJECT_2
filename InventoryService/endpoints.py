from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from inventory_repository import InventoryRepository


router = APIRouter()
product_repo = InventoryRepository(file_path='./data/inventory.json')

# Request model for product data
class InventoryCreateRequest(BaseModel):
    merchantId: int
    productName: str
    price: float
    quantity: int

# Endpoint to create a product
@router.post("/products", status_code=201)
async def create_product(product: InventoryCreateRequest):
    product_id = product_repo.save_product(
        merchant_id=product.merchantId,
        product_name=product.productName,
        price=product.price,
        quantity=product.quantity
    )
    return {"product_id": product_id}

# Endpoint to retrieve a Product by ID
@router.get("/products/{id}", status_code=200)
async def get_product(id: str):
    product = product_repo.get_product(id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product does not exist")
    return product

@router.put("/products/{id}", status_code=200)
async def update_product(id: str):
   product_id, product = product_repo.update_product(id)
   if product is None:
       raise HTTPException(status_code=404, detail="Product does not exist")
   return {"product_id": product_id}
