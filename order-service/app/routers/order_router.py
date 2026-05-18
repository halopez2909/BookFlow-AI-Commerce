import uuid
from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.infrastructure.database import get_db
from app.infrastructure.repositories import OrderRepositoryPostgres
from app.infrastructure.clients.inventory_client import InventoryClient
from app.application.use_cases import CreateOrder, GetOrder, GetCustomerOrders, UpdateOrderStatus
from app.domain.schemas import CreateOrderRequest, UpdateOrderStatusRequest

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("", status_code=201)
async def create_order(request: CreateOrderRequest, db: Session = Depends(get_db)):
    repo = OrderRepositoryPostgres(db)
    client = InventoryClient()
    return await CreateOrder(repo, client).execute(request)


@router.get("/{order_id}")
def get_order(order_id: uuid.UUID, db: Session = Depends(get_db)):
    repo = OrderRepositoryPostgres(db)
    return GetOrder(repo).execute(order_id)


@router.get("")
def get_orders(customer_id: Optional[str] = None, db: Session = Depends(get_db)):
    repo = OrderRepositoryPostgres(db)
    if customer_id:
        return GetCustomerOrders(repo).execute(customer_id)
    return []


@router.put("/{order_id}/status")
async def update_order_status(
    order_id: uuid.UUID,
    request: UpdateOrderStatusRequest,
    db: Session = Depends(get_db)
):
    repo = OrderRepositoryPostgres(db)
    client = InventoryClient()
    return await UpdateOrderStatus(repo, client).execute(order_id, request)
