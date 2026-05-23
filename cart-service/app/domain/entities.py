from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import List


@dataclass(frozen=True)
class CartItem:
    id: int | None
    cart_id: int | None
    book_id: str
    quantity: int
    unit_price: Decimal

    @property
    def subtotal(self) -> Decimal:
        return self.unit_price * self.quantity


@dataclass(frozen=True)
class CartTotal:
    amount: Decimal


@dataclass
class Cart:
    id: int | None
    customer_id: str
    status: str = "active"
    created_at: datetime | None = None
    updated_at: datetime | None = None
    items: List[CartItem] = field(default_factory=list)

    @property
    def total(self) -> CartTotal:
        total_amount = sum((item.subtotal for item in self.items), Decimal("0.00"))
        return CartTotal(amount=total_amount)
