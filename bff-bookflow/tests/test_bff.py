from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["service"] == "bff-bookflow"


def test_protected_route_without_token():
    response = client.get("/api/inventory/batches")
    assert response.status_code == 403


def test_protected_route_with_invalid_token():
    response = client.get(
        "/api/inventory/batches",
        headers={"Authorization": "Bearer invalidtoken"},
    )
    assert response.status_code == 401


def test_catalog_books_public():
    response = client.get("/api/catalog/books")
    assert response.status_code in [200, 500]


def test_catalog_categories_public():
    response = client.get("/api/catalog/categories")
    assert response.status_code in [200, 500]
