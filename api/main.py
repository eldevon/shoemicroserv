# api/main.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import httpx

app = FastAPI(title="Shoe Store API Gateway")

class ShoeItem(BaseModel):
    shoe_id: str
    name: str
    quantity: int
    price: float

class OrderRequest(BaseModel):
    items: List[ShoeItem]
    total_amount: float
    user_id: str

@app.post("/orders/")
async def create_order(order: OrderRequest):
    # Forward to order service
    async with httpx.AsyncClient() as client:
        # Step 1: Create order (order service)
        order_resp = await client.post(
            "http://order:8001/orders/",
            json=order.dict()
        )
        if order_resp.status_code != 200:
            return {"error": "Order creation failed", "detail": order_resp.json()}

        order_data = order_resp.json()
        order_id = order_data["order_id"]

        # Step 2: Process payment (payment service)
        payment_resp = await client.post(
            "http://payment:8002/payments/",
            json={"order_id": order_id, "amount": order.total_amount}
        )
        if payment_resp.status_code != 200:
            # TODO: compensate (rollback order) — omitted for minimalism
            return {"error": "Payment failed", "detail": payment_resp.json()}

        return {
            "order_id": order_id,
            "status": "confirmed",
            "message": "Order placed and paid successfully"
        }
        