from model import Merchant
import uvicorn
from typing import Dict, List
from fastapi import FastAPI, HTTPException, status
import json 



app = FastAPI()
uvi = uvicorn()

merchant = Merchant()

DATABASE_FILE = "./MerchantDB.json"

def read_merchants(file_path: str):

    with open(file_path, 'r') as f:
        return json.load(f)

def save_merchants(merchants: List[Dict]) -> None:

    with open (DATABASE_FILE, 'w') as data_file:
        json.dump(merchants, data_file)


#temp database
merchants_db = {merchant["id"]: merchant for merchant in read_merchants(DATABASE_FILE)}


@app.post("/merchant/", response_model=Merchant, status_code=status.HTTP_201_CREATED)
async def create_merchant(merchant: Merchant):

    if merchants_db: 

        previous_id = max(merchant["id"] for merchant in merchants_db.values()) # stærsta id er væntanlega seinasta id sem var assignað til merchant.
    else:

        previous_id = 0

    merchant_id = 1 + previous_id

    new_merchant = Merchant(id=merchant_id, **merchant.model_dump())

    merchants_db[merchant_id] = new_merchant

    save_merchants(list(merchants_db.values()))

    return new_merchant

@app.get("/merchants/{merchant_id}", response_model=Merchant)
async def get_merchant(merchant_id: int):

    merchant = merchants_db.get(merchant_id)

    if merchant is None:
        raise HTTPException(status_code=404, detail="Merchant not found")
    
    return {
        "name" : merchant["name"],
        "ssn" : merchant["ssn"],   
        "email" : merchant["email"],
        "phone_number" : merchant["phone_number"],
        "allows_discount" : merchant["allows_discount"]
    }

if __name__ == "__main__":
    uvi.run(app, host="0.0.0.0", port=8001)


