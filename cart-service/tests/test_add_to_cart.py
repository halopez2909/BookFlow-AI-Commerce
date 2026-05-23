from app.infrastructure.clients.inventory_client import InventoryClient


def test_add_to_cart_with_stock(client):
    response = client.post(
        "/cart/items",
        json={
            "customer_id": "customer-test",
            "book_id": "book-1",
            "quantity": 2,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["customer_id"] == "customer-test"
    assert data["status"] == "active"
    assert len(data["items"]) == 1
    assert data["items"][0]["book_id"] == "book-1"
    assert data["items"][0]["quantity"] == 2
    assert data["items"][0]["unit_price"] == "50000.00"
    assert data["items"][0]["subtotal"] == "100000.00"
    assert data["total"] == "100000.00"


def test_add_to_cart_without_stock_returns_409(client, monkeypatch):
    def fake_check_availability(self, book_id: str, quantity: int) -> bool:
        return False

    monkeypatch.setattr(
        InventoryClient,
        "check_availability",
        fake_check_availability,
    )

    response = client.post(
        "/cart/items",
        json={
            "customer_id": "customer-test",
            "book_id": "book-without-stock",
            "quantity": 2,
        },
    )

    assert response.status_code == 409
    assert "No hay stock suficiente" in response.json()["detail"]
