import pytest
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
