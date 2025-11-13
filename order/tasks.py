# order/tasks.py
from celery import Celery

celery_app = Celery(
    "order_worker",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

@celery_app.task
def process_order_async(order_id: str):
    # e.g., send email, update inventory — just log for now
    print(f"[Order Worker] Processing order {order_id} asynchronously")
    return f"Processed {order_id}"
    