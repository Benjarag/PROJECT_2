from pydantic import BaseModel, EmailStr

class BuyerModel(BaseModel):
    name: str
    ssn: str
    email: EmailStr
    phoneNumber: str
