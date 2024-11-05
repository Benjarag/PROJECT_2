from models.model import Merchant
import uuid
import uvicorn
from typing import Dict
from fastapi import FastAPI, HTTPException, status
import json 


app = FastAPI()

def merchant_database(file_path: str):
    with open(file_path, 'r') as f:
        return json.load(f)

#temp database 
merchants_db: Dict[str, dict] = {}

class MerhcantResponse(Merchant):
    id: str
@app.post("/merchant/", response_model=Merchant, status_code=status.HTTP_201_CREATED)
async def create_merchant(merchant: Merchant):
    merchant_id = str(uuid.uuid4())

    merchants_db[merchant_id] = merchant.model_dump()

    return {"id": merchant_id, **merchant.model_dump()}

@app.get("/merchant/{merchant_id}", response_model=Merchant)
async def get_merchant(id: str):
    merchant = merchants_db.get(id)

    if merchant is None:
        raise HTTPException(status_code=404, detail="Merchant not found")
    return {"id": id, **merchant}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
