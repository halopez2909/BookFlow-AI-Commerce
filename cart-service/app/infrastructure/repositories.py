from decimal import Decimal
from typing import Optional

from sqlalchemy.orm import Session

from app.domain.entities import Cart, CartItem
from app.domain.repositories import CartItemRepository, CartRepository
from app.infrastructure.models import CartItemModel, CartModel


def _to_cart_item(model: CartItemModel) -> CartItem:
    return CartItem(
        id=model.id,
        cart_id=model.cart_id,
        book_id=model.book_id,
        quantity=model.quantity,
        unit_price=Decimal(str(model.unit_price)),
    )


def _to_cart(model: CartModel) -> Cart:
    return Cart(
        id=model.id,
        customer_id=model.customer_id,
        status=model.status,
        created_at=model.created_at,
        updated_at=model.updated_at,
        items=[_to_cart_item(item) for item in model.items],
    )


class SQLAlchemyCartRepository(CartRepository):

    def __init__(self, db: Session):
        self.db = db

    def get_active_by_customer_id(self, customer_id: str) -> Optional[Cart]:
        model = (
            self.db.query(CartModel)
            .filter(CartModel.customer_id == customer_id, CartModel.status == "active")
            .first()
        )
        return _to_cart(model) if model else None

    def get_by_id(self, cart_id: int) -> Optional[Cart]:
        model = self.db.query(CartModel).filter(CartModel.id == cart_id).first()
        return _to_cart(model) if model else None

    def create(self, customer_id: str) -> Cart:
        model = CartModel(customer_id=customer_id, status="active")
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return _to_cart(model)

    def save(self, cart: Cart) -> Cart:
        self.db.commit()
        return self.get_by_id(cart.id)

    def clear(self, customer_id: str) -> None:
        cart = (
            self.db.query(CartModel)
            .filter(CartModel.customer_id == customer_id, CartModel.status == "active")
            .first()
        )
        if not cart:
            return

        self.db.query(CartItemModel).filter(CartItemModel.cart_id == cart.id).delete()
        self.db.commit()


class SQLAlchemyCartItemRepository(CartItemRepository):

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, item_id: int) -> Optional[CartItem]:
        model = self.db.query(CartItemModel).filter(CartItemModel.id == item_id).first()
        return _to_cart_item(model) if model else None

    def get_model_by_id(self, item_id: int) -> Optional[CartItemModel]:
        return self.db.query(CartItemModel).filter(CartItemModel.id == item_id).first()

    def get_by_cart_and_book(self, cart_id: int, book_id: str) -> Optional[CartItem]:
        model = (
            self.db.query(CartItemModel)
            .filter(CartItemModel.cart_id == cart_id, CartItemModel.book_id == book_id)
            .first()
        )
        return _to_cart_item(model) if model else None

    def add_or_update_item(
        self,
        cart_id: int,
        book_id: str,
        quantity: int,
        unit_price,
    ) -> CartItem:
        model = (
            self.db.query(CartItemModel)
            .filter(CartItemModel.cart_id == cart_id, CartItemModel.book_id == book_id)
            .first()
        )

        if model:
            model.quantity = model.quantity + quantity
            model.unit_price = Decimal(str(unit_price))
        else:
            model = CartItemModel(
                cart_id=cart_id,
                book_id=book_id,
                quantity=quantity,
                unit_price=Decimal(str(unit_price)),
            )
            self.db.add(model)

        self.db.commit()
        self.db.refresh(model)
        return _to_cart_item(model)

    def update_quantity(self, item_id: int, quantity: int) -> CartItem:
        model = self.get_model_by_id(item_id)
        if not model:
            raise ValueError("Ítem del carrito no encontrado.")

        model.quantity = quantity
        self.db.commit()
        self.db.refresh(model)
        return _to_cart_item(model)

    def remove(self, item_id: int) -> None:
        model = self.get_model_by_id(item_id)
        if not model:
            raise ValueError("Ítem del carrito no encontrado.")

        self.db.delete(model)
        self.db.commit()

    def count_distinct_items(self, cart_id: int) -> int:
        return (
            self.db.query(CartItemModel)
            .filter(CartItemModel.cart_id == cart_id)
            .count()
        )
