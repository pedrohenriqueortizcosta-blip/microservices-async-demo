from fastapi import APIRouter, HTTPException

from app.schemas.order import OrderCreate, OrderResponse
from app.services import order_store
from app.services.broker import publish_order_created

router = APIRouter()


@router.post("/", response_model=OrderResponse, status_code=201)
def create_order(payload: OrderCreate):
    order = order_store.create_order(payload.model_dump())

    event = {
        "event_type": "OrderCreated",
        "order_id": order["order_id"],
        "customer_id": order["customer_id"],
        "amount": order["amount"],
    }

    publish_order_created(event)

    return order


@router.get("/", response_model=list[OrderResponse])
def list_orders():
    return order_store.list_orders()


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: str):
    order = order_store.get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order