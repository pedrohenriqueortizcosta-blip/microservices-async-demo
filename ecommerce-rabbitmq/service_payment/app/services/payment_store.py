from datetime import datetime
from uuid import uuid4

payments_db: dict[str, dict] = {}


def create_payment(order_id: str, customer_id: int, amount: float, payment_status: str) -> dict:
    payment = {
        "payment_id": str(uuid4()),
        "order_id": order_id,
        "customer_id": customer_id,
        "amount": amount,
        "payment_status": payment_status,
        "processed_at": datetime.utcnow().isoformat(),
    }

    payments_db[payment["payment_id"]] = payment
    return payment


def list_payments() -> list[dict]:
    return list(payments_db.values())