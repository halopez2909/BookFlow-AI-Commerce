import os
from decimal import Decimal

from app.domain.entities import Cart
from app.domain.rules import CartLimitRule
from app.infrastructure.clients.inventory_client import InventoryClient
from app.infrastructure.clients.pricing_client import PricingClient
from app.infrastructure.repositories import (
    SQLAlchemyCartItemRepository,
    SQLAlchemyCartRepository,
)


class CartNotFoundError(Exception):
    pass


class CartItemNotFoundError(Exception):
    pass


class StockNotAvailableError(Exception):
    pass


class CartLimitExceededError(Exception):
    pass


class InvalidQuantityError(Exception):
    pass


def _validate_quantity(quantity: int) -> None:
    if quantity <= 0:
        raise InvalidQuantityError("La cantidad debe ser mayor a cero.")


class AddToCart:

    def __init__(
        self,
        cart_repository: SQLAlchemyCartRepository,
        cart_item_repository: SQLAlchemyCartItemRepository,
        inventory_client: InventoryClient,
        pricing_client: PricingClient,
    ):
        self.cart_repository = cart_repository
        self.cart_item_repository = cart_item_repository
        self.inventory_client = inventory_client
        self.pricing_client = pricing_client
        self.cart_limit_rule = CartLimitRule(
            max_items=int(os.getenv("CART_MAX_ITEMS", "50"))
        )

    def execute(self, customer_id: str, book_id: str, quantity: int) -> Cart:
        _validate_quantity(quantity)

        cart = self.cart_repository.get_active_by_customer_id(customer_id)
        if not cart:
            cart = self.cart_repository.create(customer_id)

        existing_item = self.cart_item_repository.get_by_cart_and_book(cart.id, book_id)
        quantity_to_validate = quantity
        is_new_item = existing_item is None

        if existing_item:
            quantity_to_validate = existing_item.quantity + quantity

        has_stock = self.inventory_client.check_availability(
            book_id=book_id,
            quantity=quantity_to_validate,
        )

        if not has_stock:
            raise StockNotAvailableError(
                f"No hay stock suficiente para el libro {book_id}."
            )

        distinct_items = self.cart_item_repository.count_distinct_items(cart.id)
        if is_new_item:
            distinct_items += 1

        try:
            self.cart_limit_rule.validate(distinct_items)
        except ValueError as exc:
            raise CartLimitExceededError(str(exc)) from exc

        unit_price = self.pricing_client.get_current_price(book_id)

        self.cart_item_repository.add_or_update_item(
            cart_id=cart.id,
            book_id=book_id,
            quantity=quantity,
            unit_price=unit_price,
        )

        return self.cart_repository.get_by_id(cart.id)


class GetCart:

    def __init__(self, cart_repository: SQLAlchemyCartRepository):
        self.cart_repository = cart_repository

    def execute(self, customer_id: str) -> Cart:
        cart = self.cart_repository.get_active_by_customer_id(customer_id)
        if not cart:
            cart = self.cart_repository.create(customer_id)
        return cart


class UpdateCartItem:

    def __init__(
        self,
        cart_repository: SQLAlchemyCartRepository,
        cart_item_repository: SQLAlchemyCartItemRepository,
        inventory_client: InventoryClient,
    ):
        self.cart_repository = cart_repository
        self.cart_item_repository = cart_item_repository
        self.inventory_client = inventory_client

    def execute(self, item_id: int, quantity: int) -> Cart:
        _validate_quantity(quantity)

        item = self.cart_item_repository.get_by_id(item_id)
        if not item:
            raise CartItemNotFoundError("Ítem del carrito no encontrado.")

        if quantity > item.quantity:
            has_stock = self.inventory_client.check_availability(
                book_id=item.book_id,
                quantity=quantity,
            )

            if not has_stock:
                raise StockNotAvailableError(
                    f"No hay stock suficiente para el libro {item.book_id}."
                )

        updated_item = self.cart_item_repository.update_quantity(item_id, quantity)
        cart = self.cart_repository.get_by_id(updated_item.cart_id)

        if not cart:
            raise CartNotFoundError("Carrito no encontrado.")

        return cart


class RemoveCartItem:

    def __init__(
        self,
        cart_repository: SQLAlchemyCartRepository,
        cart_item_repository: SQLAlchemyCartItemRepository,
    ):
        self.cart_repository = cart_repository
        self.cart_item_repository = cart_item_repository

    def execute(self, item_id: int) -> Cart:
        item = self.cart_item_repository.get_by_id(item_id)
        if not item:
            raise CartItemNotFoundError("Ítem del carrito no encontrado.")

        cart_id = item.cart_id
        self.cart_item_repository.remove(item_id)

        cart = self.cart_repository.get_by_id(cart_id)
        if not cart:
            raise CartNotFoundError("Carrito no encontrado.")

        return cart


class ClearCart:

    def __init__(self, cart_repository: SQLAlchemyCartRepository):
        self.cart_repository = cart_repository

    def execute(self, customer_id: str) -> Cart:
        self.cart_repository.clear(customer_id)
        cart = self.cart_repository.get_active_by_customer_id(customer_id)

        if not cart:
            cart = self.cart_repository.create(customer_id)

        return cart
