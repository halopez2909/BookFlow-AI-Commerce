import uuid
from typing import Optional, List
from sqlalchemy.orm import Session
from app.domain.entities import Order, OrderItem
from app.domain.repositories import OrderRepository
from app.infrastructure.models import OrderModel, OrderItemModel
from datetime import datetime


class OrderRepositoryPostgres(OrderRepository):

    def __init__(self, db: Session):
        self.db = db

    def save(self, order: Order) -> Order:
        model = OrderModel(
            id=order.id,
            customer_id=order.customer_id,
            status=order.status,
            notes=order.notes,
            created_at=order.created_at,
            updated_at=order.updated_at,
        )
        for item in order.items:
            item_model = OrderItemModel(
                id=item.id,
                order_id=order.id,
                book_id=item.book_id,
                quantity=item.quantity,
                unit_price=item.unit_price,
                title=item.title,
            )
            model.items.append(item_model)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return self._to_entity(model)

    def get_by_id(self, order_id: uuid.UUID) -> Optional[Order]:
        model = self.db.query(OrderModel).filter(OrderModel.id == order_id).first()
        return self._to_entity(model) if model else None

    def get_by_customer(self, customer_id: str) -> List[Order]:
        models = self.db.query(OrderModel).filter(OrderModel.customer_id == customer_id).all()
        return [self._to_entity(m) for m in models]

    def update(self, order: Order) -> Order:
        model = self.db.query(OrderModel).filter(OrderModel.id == order.id).first()
        model.status = order.status
        model.notes = order.notes
        model.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(model)
        return self._to_entity(model)

    def _to_entity(self, model: OrderModel) -> Order:
        items = [
            OrderItem(
                id=item.id,
                order_id=item.order_id,
                book_id=item.book_id,
                quantity=item.quantity,
                unit_price=item.unit_price,
                title=item.title,
            )
            for item in model.items
        ]
        return Order(
            id=model.id,
            customer_id=model.customer_id,
            status=model.status,
            items=items,
            created_at=model.created_at,
            updated_at=model.updated_at,
            notes=model.notes,
        )
