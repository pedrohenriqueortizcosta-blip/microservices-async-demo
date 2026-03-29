from pydantic import BaseModel, Field


class OrderCreate(BaseModel):
    customer_id: int
    product_id: int
    quantity: int = Field(gt=0)
    amount: float = Field(gt=0)


class OrderResponse(BaseModel):
    order_id: str
    customer_id: int
    product_id: int
    quantity: int
    amount: float
    status: str
    created_at: str