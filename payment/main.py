# payment/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Payment Service")

class PaymentRequest(BaseModel):
    order_id: str
    amount: float

@app.post("/payments/")
def process_payment(payment: PaymentRequest):
    # Simulate success (always for demo)
    if payment.amount <= 0:
        raise HTTPException(status_code=400, detail="Invalid amount")

    # Simulate gateway call
    print(f"[Payment] Charging ${payment.amount} for order {payment.order_id}")
    return {
        "payment_id": f"pay_{payment.order_id[:8]}",
        "status": "success",
        "message": "Payment processed"
    }
    