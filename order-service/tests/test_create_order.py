import pytest
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
