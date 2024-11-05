from pydantic import BaseModel


class Buyer(BaseModel):
    name: str
    ssn: str  # Consider using validation for the SSN format if needed
    email: str
    phoneNumber: str
