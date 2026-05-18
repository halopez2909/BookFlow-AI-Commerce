import uuid
from datetime import datetime
from typing import List, Optional
from fastapi import HTTPException
from app.domain.entities import Order, OrderItem
from app.domain.repositories import OrderRepository
from app.domain.schemas import CreateOrderRequest, UpdateOrderStatusRequest, OrderResponse, OrderItemResponse
from app.infrastructure.clients.inventory_client import InventoryClient


def _item_to_response(item: OrderItem) -> OrderItemResponse:
    return OrderItemResponse(
        id=item.id,
        order_id=item.order_id,
        book_id=item.book_id,
        quantity=item.quantity,
        unit_price=item.unit_price,
        subtotal=item.subtotal,
        title=item.title,
    )


def _order_to_response(order: Order) -> OrderResponse:
    return OrderResponse(
        id=order.id,
        customer_id=order.customer_id,
        status=order.status,
        total_amount=order.total_amount,
        items=[_item_to_response(i) for i in order.items],
        created_at=order.created_at,
        updated_at=order.updated_at,
        notes=order.notes,
    )


class CreateOrder:
    def __init__(self, repository: OrderRepository, inventory_client: InventoryClient):
        self.repository = repository
        self.inventory_client = inventory_client

    async def execute(self, request: CreateOrderRequest) -> OrderResponse:
        # Validate stock availability for all items
        failed_items = []
        for item in request.items:
            available = await self.inventory_client.check_availability(
                item.book_id, item.quantity
            )
            if not available:
                failed_items.append({
                    "book_id": item.book_id,
                    "title": item.title,
                    "requested_quantity": item.quantity,
                })

        if failed_items:
            raise HTTPException(
                status_code=409,
                detail={
                    "message": "Stock insuficiente para algunos items",
                    "failed_items": failed_items,
                }
            )

        # Create order with historical prices
        order_id = uuid.uuid4()
        items = [
            OrderItem(
                id=uuid.uuid4(),
                order_id=order_id,
                book_id=item.book_id,
                quantity=item.quantity,
                unit_price=item.unit_price,
                title=item.title,
            )
            for item in request.items
        ]

        order = Order(
            id=order_id,
            customer_id=request.customer_id,
            status="pending",
            items=items,
            notes=request.notes,
        )

        saved = self.repository.save(order)
        return _order_to_response(saved)


class GetOrder:
    def __init__(self, repository: OrderRepository):
        self.repository = repository

    def execute(self, order_id: uuid.UUID) -> OrderResponse:
        order = self.repository.get_by_id(order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Pedido no encontrado")
        return _order_to_response(order)


class GetCustomerOrders:
    def __init__(self, repository: OrderRepository):
        self.repository = repository

    def execute(self, customer_id: str) -> List[OrderResponse]:
        orders = self.repository.get_by_customer(customer_id)
        return [_order_to_response(o) for o in orders]


class UpdateOrderStatus:
    def __init__(self, repository: OrderRepository, inventory_client: InventoryClient):
        self.repository = repository
        self.inventory_client = inventory_client

    async def execute(self, order_id: uuid.UUID, request: UpdateOrderStatusRequest) -> OrderResponse:
        order = self.repository.get_by_id(order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Pedido no encontrado")

        try:
            old_status = order.status
            order.transition_to(request.status)
        except ValueError as e:
            raise HTTPException(status_code=422, detail=str(e))

        # Side effects
        if request.status == "confirmed" and old_status == "pending":
            for item in order.items:
                await self.inventory_client.deduct_stock(item.book_id, item.quantity)

        if request.status == "cancelled" and old_status == "confirmed":
            for item in order.items:
                await self.inventory_client.restore_stock(item.book_id, item.quantity)

        if request.notes:
            order.notes = request.notes

        updated = self.repository.update(order)
        return _order_to_response(updated)
