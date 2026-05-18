import pytest
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
