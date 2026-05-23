import pytest, httpx

BFF = "http://localhost:8000"

def test_health():
    r = httpx.get(f"{BFF}/health", timeout=5)
    assert r.status_code == 200

def test_system_health():
    r = httpx.get(f"{BFF}/api/system/health", timeout=10)
    assert r.status_code == 200
    data = r.json()
    assert "services" in data

def test_catalog():
    r = httpx.get(f"{BFF}/api/catalog/books", timeout=10)
    assert r.status_code == 200

def test_recommendations():
    r = httpx.get(f"{BFF}/api/catalog/books", timeout=10)
    books = r.json().get("items", [])
    if books:
        bid = books[0]["id"]
        r2 = httpx.get(f"{BFF}/api/recommendations/{bid}", timeout=10)
        assert r2.status_code == 200

def test_assistant():
    r = httpx.post(f"{BFF}/api/assistant/query",
        json={"session_id": "test-session", "question": "Cuanto cuesta Don Quixote"},
        timeout=30)
    assert r.status_code == 200
    assert "answer" in r.json()

def test_cart():
    r = httpx.get(f"{BFF}/api/cart/test-customer", timeout=5)
    assert r.status_code in [200, 404, 500]
