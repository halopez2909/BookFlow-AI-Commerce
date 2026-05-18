import requests
import pytest

ORDER_URL = "http://localhost:8010"
BASE_URL = "http://localhost:8000"

def test_order_no_stock():
    payload = {
        "customer_id": "e2e-customer-003",
        "items": [{"book_id": "REF-SIN-STOCK", "quantity": 9999, "unit_price": 10000.0, "title": "Libro Sin Stock"}],
    }
    r = requests.post(f"{ORDER_URL}/orders", json=payload, timeout=10)
    assert r.status_code == 409
    assert "failed_items" in r.json()["detail"]
    print("ERROR 1 OK: Libro sin stock retorna 409")

def test_order_invalid_state_transition():
    payload = {
        "customer_id": "e2e-customer-004",
        "items": [{"book_id": "REF-TOLKIEN", "quantity": 1, "unit_price": 20000.0, "title": "Lord of the Rings"}],
    }
    r = requests.post(f"{ORDER_URL}/orders", json=payload, timeout=10)
    assert r.status_code == 201
    order_id = r.json()["id"]

    r = requests.put(f"{ORDER_URL}/orders/{order_id}/status", json={"status": "delivered"})
    assert r.status_code == 422
    print("ERROR 2 OK: Transicion invalida retorna 422")

def test_jwt_expired_returns_401():
    fake_token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.fake.signature"
    r = requests.get(f"{BASE_URL}/api/normalization/records", headers={"Authorization": fake_token})
    assert r.status_code == 401
    print("ERROR 3 OK: JWT invalido retorna 401")
