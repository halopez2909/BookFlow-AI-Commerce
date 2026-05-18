import uuid
from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.entities import Order, OrderItem


class OrderRepository(ABC):
    @abstractmethod
    def save(self, order: Order) -> Order:
        pass

    @abstractmethod
    def get_by_id(self, order_id: uuid.UUID) -> Optional[Order]:
        pass

    @abstractmethod
    def get_by_customer(self, customer_id: str) -> List[Order]:
        pass

    @abstractmethod
    def update(self, order: Order) -> Order:
        pass
