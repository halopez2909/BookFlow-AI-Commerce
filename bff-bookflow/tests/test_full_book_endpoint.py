"""Sprint 3 - Dev 6 Jenn.
Test del endpoint Facade GET /api/books/{id}/full:
    - 4 llamadas paralelas (catalog + pricing + inventory + recommender)
    - Si catalog responde, devuelve 200 con las 4 secciones agregadas
    - Si catalog falla, devuelve 404
"""
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_books_full_returns_aggregated_payload():
    """Verifica que el endpoint agrega las 4 fuentes en una sola respuesta."""
    catalog_mock = AsyncMock(return_value={"id": "b1", "title": "Cien anos de soledad", "author": "Garcia Marquez"})
    pricing_mock = AsyncMock(return_value={"book_id": "b1", "suggested_price": 45000})
    inventory_mock = AsyncMock(return_value={"book_id": "b1", "available": True, "stock": 12})
    recs_mock = AsyncMock(return_value={"items": [{"id": f"r{i}"} for i in range(6)]})

    with patch("app.infrastructure.clients.catalog_client.CatalogClient.get_book_by_id", catalog_mock), \
         patch("app.infrastructure.clients.pricing_client.PricingClient.get_decision", pricing_mock), \
         patch("app.infrastructure.clients.inventory_client.InventoryClient.get_stock", inventory_mock), \
         patch("app.infrastructure.clients.recommender_client.RecommenderClient.get_recommendations", recs_mock):
        response = client.get("/api/books/b1/full")

    assert response.status_code == 200
    data = response.json()
    assert data["book_id"] == "b1"
    assert data["catalog"]["title"] == "Cien anos de soledad"
    assert data["pricing"]["suggested_price"] == 45000
    assert data["inventory"]["available"] is True
    assert len(data["recommendations"]["items"]) == 6
    catalog_mock.assert_awaited_once()
    pricing_mock.assert_awaited_once()
    inventory_mock.assert_awaited_once()
    recs_mock.assert_awaited_once()


def test_books_full_returns_404_when_catalog_fails():
    """Si el libro no existe en catalogo, devolvemos 404."""
    fail = AsyncMock(side_effect=Exception("not found"))
    ok_inv = AsyncMock(return_value={"available": False, "stock": 0})
    ok_pricing = AsyncMock(return_value={"suggested_price": None})
    ok_recs = AsyncMock(return_value={"items": []})
    with patch("app.infrastructure.clients.catalog_client.CatalogClient.get_book_by_id", fail), \
         patch("app.infrastructure.clients.pricing_client.PricingClient.get_decision", ok_pricing), \
         patch("app.infrastructure.clients.inventory_client.InventoryClient.get_stock", ok_inv), \
         patch("app.infrastructure.clients.recommender_client.RecommenderClient.get_recommendations", ok_recs):
        response = client.get("/api/books/no-existe/full")
    assert response.status_code == 404


def test_books_full_tolerates_partial_service_failure():
    """Si falla pricing pero catalog responde, igual devolvemos 200 con _error en pricing."""
    catalog_mock = AsyncMock(return_value={"id": "b2", "title": "El amor en los tiempos del colera"})
    pricing_mock = AsyncMock(side_effect=Exception("pricing down"))
    inventory_mock = AsyncMock(return_value={"available": True, "stock": 5})
    recs_mock = AsyncMock(return_value={"items": []})
    with patch("app.infrastructure.clients.catalog_client.CatalogClient.get_book_by_id", catalog_mock), \
         patch("app.infrastructure.clients.pricing_client.PricingClient.get_decision", pricing_mock), \
         patch("app.infrastructure.clients.inventory_client.InventoryClient.get_stock", inventory_mock), \
         patch("app.infrastructure.clients.recommender_client.RecommenderClient.get_recommendations", recs_mock):
        response = client.get("/api/books/b2/full")
    assert response.status_code == 200
    data = response.json()
    assert data["catalog"]["title"] == "El amor en los tiempos del colera"
    assert data["pricing"]["_error"] is True
