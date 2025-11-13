# order/main.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import uuid
from tasks import celery_app, process_order_async

app = FastAPI(title="Order Service")

class ShoeItem(BaseModel):
    shoe_id: str
    name: str
    quantity: int
    price: float

class OrderRequest(BaseModel):
    items: List[ShoeItem]
    total_amount: float
    user_id: str

orders = {}  # in-memory — for demo only

@app.post("/orders/")
def create_order(order: OrderRequest):
    order_id = str(uuid.uuid4())
    orders[order_id] = {
        "id": order_id,
        "items": [item.dict() for item in order.items],
        "total": order.total_amount,
        "user_id": order.user_id,
        "status": "created"
    }

    # Offload async work
    process_order_async.delay(order_id)

    return {"order_id": order_id, "status": "created", "message": "Order created"}

    