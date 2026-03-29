from fastapi import FastAPI

from app.consumers.payment_result_consumer import start_payment_result_consumer
from app.routers.orders import router as orders_router

app = FastAPI(
    title="service_order",
    version="1.0.0",
)

app.include_router(orders_router, prefix="/orders", tags=["orders"])


@app.get("/health", tags=["health"])
def health():
    return {"status": "ok", "service": "order"}


@app.on_event("startup")
def startup():
    start_payment_result_consumer()