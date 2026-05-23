import os

BASE = "order-service"

files = {}

# ── Dockerfile ────────────────────────────────────────────────────────
files["Dockerfile"] = """FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8010"]
"""

# ── requirements.txt ──────────────────────────────────────────────────
files["requirements.txt"] = """fastapi==0.111.0
uvicorn==0.29.0
sqlalchemy==2.0.30
psycopg2-binary==2.9.9
pydantic==2.7.1
pydantic-settings==2.2.1
httpx==0.27.0
python-dotenv==1.0.1
alembic==1.13.1
pytest==8.2.0
pytest-mock==3.14.0
pytest-asyncio==0.23.6
"""

# ── .env.example ──────────────────────────────────────────────────────
files[".env.example"] = """DATABASE_URL=postgresql://bookflow:bookflow123@postgres:5432/order_db
INVENTORY_URL=http://inventory-service:8002
CATALOG_URL=http://catalog-service:8003
AUTH_URL=http://auth-service:8001
"""

# ── .env ──────────────────────────────────────────────────────────────
files[".env"] = """DATABASE_URL=postgresql://bookflow:bookflow123@postgres:5432/order_db
INVENTORY_URL=http://inventory-service:8002
CATALOG_URL=http://catalog-service:8003
AUTH_URL=http://auth-service:8001
"""

# ── app/__init__.py ───────────────────────────────────────────────────
files["app/__init__.py"] = ""

# ── app/main.py ───────────────────────────────────────────────────────
files["app/main.py"] = """from fastapi import FastAPI
from app.infrastructure.database import Base, engine
from app.routers import order_router

app = FastAPI(title="Order Service", version="1.0.0")

Base.metadata.create_all(bind=engine)

app.include_router(order_router.router)

@app.get("/health")
def health():
    return {"status": "ok", "service": "order-service"}
"""

# ── app/domain/__init__.py ────────────────────────────────────────────
files["app/domain/__init__.py"] = ""

# ── app/domain/entities.py ───────────────────────────────────────────
files["app/domain/entities.py"] = """import uuid
from datetime import datetime
from typing import Optional, List
from app.domain.states import OrderState, PendingState


class OrderItem:
    def __init__(
        self,
        id: uuid.UUID,
        order_id: uuid.UUID,
        book_id: str,
        quantity: int,
        unit_price: float,
        title: Optional[str] = None,
    ):
        self.id = id
        self.order_id = order_id
        self.book_id = book_id
        self.quantity = quantity
        self.unit_price = unit_price
        self.title = title

    @property
    def subtotal(self) -> float:
        return self.quantity * self.unit_price


class Order:
    def __init__(
        self,
        id: uuid.UUID,
        customer_id: str,
        status: str,
        items: List[OrderItem],
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        notes: Optional[str] = None,
    ):
        self.id = id
        self.customer_id = customer_id
        self.status = status
        self.items = items
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
        self.notes = notes

    @property
    def total_amount(self) -> float:
        return sum(item.subtotal for item in self.items)

    def get_state(self) -> OrderState:
        from app.domain.states import (
            PendingState, ConfirmedState, ShippedState,
            DeliveredState, CancelledState
        )
        states = {
            "pending": PendingState(),
            "confirmed": ConfirmedState(),
            "shipped": ShippedState(),
            "delivered": DeliveredState(),
            "cancelled": CancelledState(),
        }
        return states.get(self.status, PendingState())

    def transition_to(self, new_status: str) -> None:
        state = self.get_state()
        state.validate_transition(new_status)
        self.status = new_status
        self.updated_at = datetime.utcnow()
"""

# ── app/domain/states.py ─────────────────────────────────────────────
files["app/domain/states.py"] = """from abc import ABC, abstractmethod


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
"""

# ── app/domain/repositories.py ───────────────────────────────────────
files["app/domain/repositories.py"] = """import uuid
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
"""

# ── app/domain/schemas.py ─────────────────────────────────────────────
files["app/domain/schemas.py"] = """import uuid
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class OrderItemRequest(BaseModel):
    book_id: str
    quantity: int
    unit_price: float
    title: Optional[str] = None


class CreateOrderRequest(BaseModel):
    customer_id: str
    items: List[OrderItemRequest]
    notes: Optional[str] = None


class UpdateOrderStatusRequest(BaseModel):
    status: str
    notes: Optional[str] = None


class OrderItemResponse(BaseModel):
    id: uuid.UUID
    order_id: uuid.UUID
    book_id: str
    quantity: int
    unit_price: float
    subtotal: float
    title: Optional[str] = None

    model_config = {"from_attributes": True}


class OrderResponse(BaseModel):
    id: uuid.UUID
    customer_id: str
    status: str
    total_amount: float
    items: List[OrderItemResponse]
    created_at: datetime
    updated_at: datetime
    notes: Optional[str] = None

    model_config = {"from_attributes": True}
"""

# ── app/infrastructure/__init__.py ───────────────────────────────────
files["app/infrastructure/__init__.py"] = ""

# ── app/infrastructure/database.py ───────────────────────────────────
files["app/infrastructure/database.py"] = """import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://bookflow:bookflow123@localhost:5432/order_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
"""

# ── app/infrastructure/models.py ─────────────────────────────────────
files["app/infrastructure/models.py"] = """import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.infrastructure.database import Base


class OrderModel(Base):
    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(String, nullable=False, index=True)
    status = Column(String, nullable=False, default="pending")
    notes = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    items = relationship("OrderItemModel", back_populates="order", cascade="all, delete-orphan")


class OrderItemModel(Base):
    __tablename__ = "order_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"), nullable=False)
    book_id = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    title = Column(String, nullable=True)

    order = relationship("OrderModel", back_populates="items")
"""

# ── app/infrastructure/repositories.py ───────────────────────────────
files["app/infrastructure/repositories.py"] = """import uuid
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
"""

# ── app/infrastructure/clients/__init__.py ────────────────────────────
files["app/infrastructure/clients/__init__.py"] = ""

# ── app/infrastructure/clients/inventory_client.py ───────────────────
files["app/infrastructure/clients/inventory_client.py"] = """import os
import httpx
from dotenv import load_dotenv

load_dotenv()

INVENTORY_URL = os.getenv("INVENTORY_URL", "http://inventory-service:8002")


class InventoryClient:

    async def check_availability(self, book_id: str, quantity: int) -> bool:
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                r = await client.get(f"{INVENTORY_URL}/inventory/books/{book_id}")
                if r.status_code != 200:
                    return False
                data = r.json()
                available = data.get("quantity", 0)
                return available >= quantity
        except Exception:
            return False

    async def deduct_stock(self, book_id: str, quantity: int) -> bool:
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                r = await client.post(
                    f"{INVENTORY_URL}/inventory/books/{book_id}/deduct",
                    json={"quantity": quantity}
                )
                return r.status_code in [200, 201]
        except Exception:
            return False

    async def restore_stock(self, book_id: str, quantity: int) -> bool:
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                r = await client.post(
                    f"{INVENTORY_URL}/inventory/books/{book_id}/restore",
                    json={"quantity": quantity}
                )
                return r.status_code in [200, 201]
        except Exception:
            return False
"""

# ── app/application/__init__.py ───────────────────────────────────────
files["app/application/__init__.py"] = ""

# ── app/application/use_cases.py ─────────────────────────────────────
files["app/application/use_cases.py"] = """import uuid
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
"""

# ── app/routers/__init__.py ───────────────────────────────────────────
files["app/routers/__init__.py"] = ""

# ── app/routers/order_router.py ──────────────────────────────────────
files["app/routers/order_router.py"] = """import uuid
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
"""

# ── tests/__init__.py ─────────────────────────────────────────────────
files["tests/__init__.py"] = ""

# ── tests/test_create_order.py ───────────────────────────────────────
files["tests/test_create_order.py"] = """import pytest
import uuid
from unittest.mock import AsyncMock, MagicMock
from app.application.use_cases import CreateOrder
from app.domain.schemas import CreateOrderRequest, OrderItemRequest
from fastapi import HTTPException


@pytest.fixture
def mock_repo():
    repo = MagicMock()
    return repo


@pytest.fixture
def mock_inventory():
    client = MagicMock()
    client.check_availability = AsyncMock(return_value=True)
    client.deduct_stock = AsyncMock(return_value=True)
    return client


@pytest.mark.asyncio
async def test_create_order_success(mock_repo, mock_inventory):
    from app.domain.entities import Order, OrderItem
    from datetime import datetime

    order_id = uuid.uuid4()
    mock_repo.save.return_value = Order(
        id=order_id,
        customer_id="customer-001",
        status="pending",
        items=[
            OrderItem(
                id=uuid.uuid4(),
                order_id=order_id,
                book_id="book-001",
                quantity=2,
                unit_price=25000.0,
                title="Clean Code",
            )
        ],
    )

    request = CreateOrderRequest(
        customer_id="customer-001",
        items=[
            OrderItemRequest(
                book_id="book-001",
                quantity=2,
                unit_price=25000.0,
                title="Clean Code",
            )
        ],
    )

    use_case = CreateOrder(mock_repo, mock_inventory)
    result = await use_case.execute(request)

    assert result.customer_id == "customer-001"
    assert result.status == "pending"
    assert result.total_amount == 50000.0
    mock_inventory.check_availability.assert_called_once_with("book-001", 2)


@pytest.mark.asyncio
async def test_create_order_no_stock(mock_repo, mock_inventory):
    mock_inventory.check_availability = AsyncMock(return_value=False)

    request = CreateOrderRequest(
        customer_id="customer-001",
        items=[
            OrderItemRequest(
                book_id="book-sin-stock",
                quantity=10,
                unit_price=25000.0,
                title="Libro Agotado",
            )
        ],
    )

    use_case = CreateOrder(mock_repo, mock_inventory)

    with pytest.raises(HTTPException) as exc_info:
        await use_case.execute(request)

    assert exc_info.value.status_code == 409
    assert "failed_items" in exc_info.value.detail
"""

# ── tests/test_order_status.py ───────────────────────────────────────
files["tests/test_order_status.py"] = """import pytest
import uuid
from unittest.mock import AsyncMock, MagicMock
from app.domain.entities import Order, OrderItem
from app.application.use_cases import UpdateOrderStatus
from app.domain.schemas import UpdateOrderStatusRequest
from fastapi import HTTPException


def make_order(status: str) -> Order:
    order_id = uuid.uuid4()
    return Order(
        id=order_id,
        customer_id="customer-001",
        status=status,
        items=[
            OrderItem(
                id=uuid.uuid4(),
                order_id=order_id,
                book_id="book-001",
                quantity=1,
                unit_price=25000.0,
            )
        ],
    )


@pytest.fixture
def mock_repo():
    return MagicMock()


@pytest.fixture
def mock_inventory():
    client = MagicMock()
    client.deduct_stock = AsyncMock(return_value=True)
    client.restore_stock = AsyncMock(return_value=True)
    return client


@pytest.mark.asyncio
async def test_valid_transition_pending_to_confirmed(mock_repo, mock_inventory):
    order = make_order("pending")
    mock_repo.get_by_id.return_value = order
    mock_repo.update.return_value = Order(
        id=order.id, customer_id=order.customer_id,
        status="confirmed", items=order.items
    )

    use_case = UpdateOrderStatus(mock_repo, mock_inventory)
    result = await use_case.execute(order.id, UpdateOrderStatusRequest(status="confirmed"))

    assert result.status == "confirmed"
    mock_inventory.deduct_stock.assert_called_once()


@pytest.mark.asyncio
async def test_invalid_transition_pending_to_delivered(mock_repo, mock_inventory):
    order = make_order("pending")
    mock_repo.get_by_id.return_value = order

    use_case = UpdateOrderStatus(mock_repo, mock_inventory)

    with pytest.raises(HTTPException) as exc_info:
        await use_case.execute(order.id, UpdateOrderStatusRequest(status="delivered"))

    assert exc_info.value.status_code == 422


@pytest.mark.asyncio
async def test_cancel_confirmed_restores_stock(mock_repo, mock_inventory):
    order = make_order("confirmed")
    mock_repo.get_by_id.return_value = order
    mock_repo.update.return_value = Order(
        id=order.id, customer_id=order.customer_id,
        status="cancelled", items=order.items
    )

    use_case = UpdateOrderStatus(mock_repo, mock_inventory)
    result = await use_case.execute(order.id, UpdateOrderStatusRequest(status="cancelled"))

    assert result.status == "cancelled"
    mock_inventory.restore_stock.assert_called_once()
"""

# ── tests/test_stock_deduction.py ────────────────────────────────────
files["tests/test_stock_deduction.py"] = """import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.infrastructure.clients.inventory_client import InventoryClient


@pytest.mark.asyncio
async def test_check_availability_sufficient_stock():
    client = InventoryClient()
    with patch("httpx.AsyncClient") as mock_client:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"quantity": 10}
        mock_client.return_value.__aenter__.return_value.get = AsyncMock(return_value=mock_response)
        result = await client.check_availability("book-001", 5)
        assert result is True


@pytest.mark.asyncio
async def test_check_availability_insufficient_stock():
    client = InventoryClient()
    with patch("httpx.AsyncClient") as mock_client:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"quantity": 2}
        mock_client.return_value.__aenter__.return_value.get = AsyncMock(return_value=mock_response)
        result = await client.check_availability("book-001", 5)
        assert result is False


@pytest.mark.asyncio
async def test_check_availability_service_down():
    client = InventoryClient()
    with patch("httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value.get = AsyncMock(side_effect=Exception("Connection refused"))
        result = await client.check_availability("book-001", 1)
        assert result is False
"""

# Write all files
for path, content in files.items():
    full_path = os.path.join(BASE, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"OK: {path}")

print("\nOrder Service creado!")
