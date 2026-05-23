from abc import ABC, abstractmethod


class CartRule(ABC):

    @abstractmethod
    def validate(self, current_distinct_items: int) -> None:
        pass


class CartLimitRule(CartRule):

    def __init__(self, max_items: int):
        self.max_items = max_items

    def validate(self, current_distinct_items: int) -> None:
        if current_distinct_items > self.max_items:
            raise ValueError(
                f"El carrito no puede superar {self.max_items} ítems distintos."
            )
