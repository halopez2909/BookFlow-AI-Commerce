from abc import ABC, abstractmethod
from typing import Optional

from app.domain.entities import Cart, CartItem


class CartRepository(ABC):

    @abstractmethod
    def get_active_by_customer_id(self, customer_id: str) -> Optional[Cart]:
        pass

    @abstractmethod
    def get_by_id(self, cart_id: int) -> Optional[Cart]:
        pass

    @abstractmethod
    def create(self, customer_id: str) -> Cart:
        pass

    @abstractmethod
    def save(self, cart: Cart) -> Cart:
        pass

    @abstractmethod
    def clear(self, customer_id: str) -> None:
        pass


class CartItemRepository(ABC):

    @abstractmethod
    def get_by_id(self, item_id: int) -> Optional[CartItem]:
        pass

    @abstractmethod
    def add_or_update_item(
        self,
        cart_id: int,
        book_id: str,
        quantity: int,
        unit_price,
    ) -> CartItem:
        pass

    @abstractmethod
    def update_quantity(self, item_id: int, quantity: int) -> CartItem:
        pass

    @abstractmethod
    def remove(self, item_id: int) -> None:
        pass

    @abstractmethod
    def count_distinct_items(self, cart_id: int) -> int:
        pass
