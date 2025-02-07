from pydantic import BaseModel

class ListSchema(BaseModel):
    name: str
    price: float
    amount: int