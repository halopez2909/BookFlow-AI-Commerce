import uuid
from datetime import datetime
from typing import Optional, List
from app.domain.states import OrderState, PendingState


class OrderItem:
    def __init__(
        self,
        id: uuid.UUID,
        order_id: uuid.UUID,
        book_id: str,
        quantity: int,
        unit_price: float,
        title: Optional[str] = None,
    ):
        self.id = id
        self.order_id = order_id
        self.book_id = book_id
        self.quantity = quantity
        self.unit_price = unit_price
        self.title = title

    @property
    def subtotal(self) -> float:
        return self.quantity * self.unit_price


class Order:
    def __init__(
        self,
        id: uuid.UUID,
        customer_id: str,
        status: str,
        items: List[OrderItem],
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        notes: Optional[str] = None,
    ):
        self.id = id
        self.customer_id = customer_id
        self.status = status
        self.items = items
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
        self.notes = notes

    @property
    def total_amount(self) -> float:
        return sum(item.subtotal for item in self.items)

    def get_state(self) -> OrderState:
        from app.domain.states import (
            PendingState, ConfirmedState, ShippedState,
            DeliveredState, CancelledState
        )
        states = {
            "pending": PendingState(),
            "confirmed": ConfirmedState(),
            "shipped": ShippedState(),
            "delivered": DeliveredState(),
            "cancelled": CancelledState(),
        }
        return states.get(self.status, PendingState())

    def transition_to(self, new_status: str) -> None:
        state = self.get_state()
        state.validate_transition(new_status)
        self.status = new_status
        self.updated_at = datetime.utcnow()
