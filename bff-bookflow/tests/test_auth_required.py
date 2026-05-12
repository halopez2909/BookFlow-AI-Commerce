"""Sprint 3 - Dev 6 Jenn.
Test de proteccion JWT en rutas privadas y rutas publicas:
    - cart, orders         -> requieren JWT (401/403 sin token)
    - assistant, recommender, books-full -> publicas
"""
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from jose import jwt

import main as main_module
from main import app


def _reset_limiter():
    main_module.global_limiter.reset()


def _make_token():
    """Genera un JWT valido para usar en los tests positivos."""
    return jwt.encode(
        {"sub": "user-1", "user_id": "user-1", "role": "customer"},
        "supersecretkey123bookflow",
        algorithm="HS256",
    )


client = TestClient(app)


def test_cart_requires_jwt():
    _reset_limiter()
    r = client.get("/api/cart/customer-1")
    assert r.status_code in (401, 403)


def test_cart_with_invalid_jwt():
    _reset_limiter()
    r = client.get(
        "/api/cart/customer-1",
        headers={"Authorization": "Bearer not-a-real-jwt"},
    )
    assert r.status_code == 401


def test_orders_requires_jwt():
    _reset_limiter()
    r = client.get("/api/orders/o-1")
    assert r.status_code in (401, 403)


def test_post_orders_requires_jwt():
    _reset_limiter()
    r = client.post("/api/orders", json={"customer_id": "c1", "items": []})
    assert r.status_code in (401, 403)


def test_cart_with_valid_jwt_calls_downstream():
    _reset_limiter()
    token = _make_token()
    mock = AsyncMock(return_value={"customer_id": "user-1", "items": []})
    with patch("app.infrastructure.clients.cart_client.CartClient.get_cart", mock):
        r = client.get(
            "/api/cart/user-1",
            headers={"Authorization": f"Bearer {token}"},
        )
    assert r.status_code == 200
    assert r.json()["customer_id"] == "user-1"


def test_assistant_is_public():
    _reset_limiter()
    mock = AsyncMock(return_value={"answer": "hola", "session_id": "s-1"})
    with patch("app.infrastructure.clients.assistant_client.AssistantClient.query", mock):
        r = client.post("/api/assistant/query", json={"query": "Recomiendame un libro"})
    assert r.status_code == 200
    assert "answer" in r.json()


def test_recommendations_popular_is_public():
    _reset_limiter()
    mock = AsyncMock(return_value={"items": [{"id": "x"}]})
    with patch("app.infrastructure.clients.recommender_client.RecommenderClient.get_popular", mock):
        r = client.get("/api/recommendations/popular")
    assert r.status_code == 200


def test_books_full_is_public():
    _reset_limiter()
    cat_m = AsyncMock(return_value={"id": "b1", "title": "X"})
    pri_m = AsyncMock(return_value={"suggested_price": 1})
    inv_m = AsyncMock(return_value={"available": True})
    rec_m = AsyncMock(return_value={"items": []})
    with patch("app.infrastructure.clients.catalog_client.CatalogClient.get_book_by_id", cat_m), \
         patch("app.infrastructure.clients.pricing_client.PricingClient.get_decision", pri_m), \
         patch("app.infrastructure.clients.inventory_client.InventoryClient.get_stock", inv_m), \
         patch("app.infrastructure.clients.recommender_client.RecommenderClient.get_recommendations", rec_m):
        r = client.get("/api/books/b1/full")
    assert r.status_code == 200
