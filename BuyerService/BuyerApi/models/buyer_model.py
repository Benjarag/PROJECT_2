from pydantic import BaseModel

class Buyer(BaseModel):
    name: str
    ssn: str
    email: str
    phone_number: str

