from pydantic import BaseModel


class Merchant(BaseModel):
    name: str
    ssn: str
    email: str
    phoneNumber: str
    allowsDiscount: bool