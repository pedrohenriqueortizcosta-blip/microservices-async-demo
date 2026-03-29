from fastapi import FastAPI

from app.consumers.order_created_consumer import start_order_created_consumer
from app.services.payment_store import list_payments

app = FastAPI(
    title="service_payment",
    version="1.0.0",
)


@app.get("/health", tags=["health"])
def health():
    return {"status": "ok", "service": "payment"}


@app.get("/payments", tags=["payments"])
def get_payments():
    return list_payments()


@app.on_event("startup")
def startup():
    start_order_created_consumer()