import uuid
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class OrderItemRequest(BaseModel):
    book_id: str
    quantity: int
    unit_price: float
    title: Optional[str] = None


class CreateOrderRequest(BaseModel):
    customer_id: str
    items: List[OrderItemRequest]
    notes: Optional[str] = None


class UpdateOrderStatusRequest(BaseModel):
    status: str
    notes: Optional[str] = None


class OrderItemResponse(BaseModel):
    id: uuid.UUID
    order_id: uuid.UUID
    book_id: str
    quantity: int
    unit_price: float
    subtotal: float
    title: Optional[str] = None

    model_config = {"from_attributes": True}


class OrderResponse(BaseModel):
    id: uuid.UUID
    customer_id: str
    status: str
    total_amount: float
    items: List[OrderItemResponse]
    created_at: datetime
    updated_at: datetime
    notes: Optional[str] = None

    model_config = {"from_attributes": True}
