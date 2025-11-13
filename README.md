# shoemicroserv
A minimal microservices backend for a shoe ecommerce system. Built with Python (FastAPI), Redis, and Celery — structured as decoupled microservices. A prototype backend.

Client
   │
   ▼
[ API Gateway ]          ← orchestrates workflow
   ├───► [ Order Service ]   ← creates orders + async tasks (Celery)
   └───► [ Payment Service ] ← simulates payment processing
           ▲
           │
        [ Redis ] ← message broker & Celery result backend

api
8000
Entry point (creates order + payment)

order
8001
Manages orders, uses Celery/Redis

payment
8002
Simulates payment processing

redis
6379
Broker for Celery (in-memory)

Quick Start
Prerequisites
Docker & Docker Compose (v2+)

git clone <this-repo>
cd shoe-store
docker-compose up --build


API Usage
Place an Order

curl -X POST http://localhost:8000/orders/ \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "usr_abc123",
    "total_amount": 89.99,
    "items": [
      {
        "shoe_id": "adidas-ultra-01",
        "name": "Adidas Ultraboost",
        "quantity": 1,
        "price": 89.99
      }
    ]
  }'


Success Response:

{
"order_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
"status": "confirmed",
"message": "Order placed and paid successfully"
}

Error Cases
400 — Invalid payment amount (≤ 0)
500 — Order/payment service failure (check logs)

🧠 In-memory state: Orders are stored in a Python dict — restarts wipe data.
💳 Payment is simulated: Always succeeds if amount > 0.
🐇 Celery tasks run in same process (not separate worker) for simplicity.
🔐 No auth, rate-limiting, or validation — add as needed.
🗃️ No database: Replace orders = {} with PostgreSQL/Mongo for persistence.
