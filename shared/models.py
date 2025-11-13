# shared/models.py
from pydantic import BaseModel
from typing import List

class ShoeItem(BaseModel):
    shoe_id: str
    name: str
    quantity: int
    price: float

class OrderRequest(BaseModel):
    items: List[ShoeItem]
    total_amount: float
    user_id: str

class OrderResponse(BaseModel):
    order_id: str
    status: str
    message: str
    