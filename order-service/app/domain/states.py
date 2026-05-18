from abc import ABC, abstractmethod


class OrderState(ABC):
    @abstractmethod
    def allowed_transitions(self) -> list:
        pass

    def validate_transition(self, new_status: str) -> None:
        if new_status not in self.allowed_transitions():
            raise ValueError(
                f"Transicion invalida: {self.__class__.__name__} -> {new_status}. "
                f"Transiciones permitidas: {self.allowed_transitions()}"
            )


class PendingState(OrderState):
    def allowed_transitions(self) -> list:
        return ["confirmed", "cancelled"]


class ConfirmedState(OrderState):
    def allowed_transitions(self) -> list:
        return ["shipped", "cancelled"]


class ShippedState(OrderState):
    def allowed_transitions(self) -> list:
        return ["delivered"]


class DeliveredState(OrderState):
    def allowed_transitions(self) -> list:
        return []


class CancelledState(OrderState):
    def allowed_transitions(self) -> list:
        return []
