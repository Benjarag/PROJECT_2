from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel
import json
import os

app = FastAPI()

class Product(BaseModel):
    merchantId: int
    productName: str
    price: float
    quantity: int
    reserved: int = 0



class InventoryManagement:
    def __init__(self) -> None:
        self.FILE_PATH = 'inventoryDB.json'
        self.initialize_file()

    def initialize_file(self):
        # Check if the file exists, if not, create it
        if not os.path.exists(self.FILE_PATH):
            with open(self.FILE_PATH, 'w') as file:
                json.dump([], file)  # Initialize with an empty list
        # Check if the file is empty
        elif os.path.getsize(self.FILE_PATH) == 0:
            with open(self.FILE_PATH, 'w') as file:
                json.dump([], file)  # Reinitialize if empty

    def get_all_inventory(self):
        with open(self.FILE_PATH, 'r') as file:
            return json.load(file)
    
    def save_inventory(self, inventory):
        with open(self.FILE_PATH, 'w') as file:
            json.dump(inventory, file, indent=4)  # inventory should be the second argument


    def add_product(self, product: Product):
        inventory = self.get_all_inventory()
        inventory.append(product)
        self.save_inventory(inventory)
    
    def get_product_with_id(self, product_id: int):
        inventory = self.get_all_inventory()
        for i in inventory:
            if i['merchantId'] == product_id:
                return i
        return None
    
inventory_manager = InventoryManagement()

@app.post("/products", status_code=201)
async def create_product(product: Product):
    inventory_manager.add_product(product.dict())

@app.get("/products", status_code=200)
async def get_all_product():
    return inventory_manager.get_all_inventory()

@app.get("/products/{id}", status_code=200)
async def get_product_by_id(id: int):
    product = inventory_manager.get_product_with_id(id)
    if product is None:
        raise HTTPException(status_code=404, detail='Product does not exist')
    return product

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)