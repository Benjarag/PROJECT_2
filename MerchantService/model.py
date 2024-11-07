
from pydantic import BaseModel

class Merchant(BaseModel):
    id: int 
    name: str
    ssn: str
    email: str
    phone_number: str 
    allows_discount: bool
