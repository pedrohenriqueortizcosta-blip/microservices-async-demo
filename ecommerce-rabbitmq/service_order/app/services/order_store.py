from datetime import datetime
from uuid import uuid4

orders_db: dict[str, dict] = {}


def create_order(data: dict) -> dict:
    order_id = str(uuid4())

    order = {
        "order_id": order_id,
        "customer_id": data["customer_id"],
        "product_id": data["product_id"],
        "quantity": data["quantity"],
        "amount": data["amount"],
        "status": "PENDING_PAYMENT",
        "created_at": datetime.utcnow().isoformat(),
    }

    orders_db[order_id] = order
    return order


def get_order(order_id: str) -> dict | None:
    return orders_db.get(order_id)


def list_orders() -> list[dict]:
    return list(orders_db.values())


def update_order_status(order_id: str, status: str) -> None:
    if order_id in orders_db:
        orders_db[order_id]["status"] = status