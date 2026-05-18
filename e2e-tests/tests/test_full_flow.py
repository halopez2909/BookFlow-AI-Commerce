import requests
import pytest
import time

BASE_URL = "http://localhost:8000"
ENRICHMENT_URL = "http://localhost:8004"
PRICING_URL = "http://localhost:8008"
ORDER_URL = "http://localhost:8010"
BATCH_ID = "10076ee3-11e3-412d-8445-b267eef7cfdd"

def test_step1_login():
    r = requests.post(f"{BASE_URL}/api/auth/login", json={"email": "admin@bookflow.com", "password": "admin1234"})
    assert r.status_code == 200
    assert "access_token" in r.json()
    print("PASO 1 OK: Login exitoso")

def test_step2_catalog_has_books(auth_headers):
    r = requests.get(f"{BASE_URL}/api/catalog/books", params={"page_size": 5}, headers=auth_headers)
    assert r.status_code == 200
    data = r.json()
    assert data["total"] > 0, "El catalogo no tiene libros"
    print(f"PASO 2 OK: {data['total']} libros en el catalogo")

def test_step3_enrichment_works():
    payload = {
        "book_reference": "e2e-test-001",
        "title": "Clean Code",
        "author": "Robert Martin",
        "isbn": "9780132350884"
    }
    r = requests.post(f"{ENRICHMENT_URL}/enrichment/enrich", json=payload, timeout=15)
    assert r.status_code == 201
    result = r.json()
    assert result.get("cover_url") or result.get("normalized_author")
    print("PASO 3 OK: Enriquecimiento con IA funcionando")

def test_step4_pricing_works():
    payload = {
        "book_reference": "e2e-test-001",
        "isbn": "9780132350884",
        "condition": "good",
        "category": "technical",
        "title": "Clean Code"
    }
    r = requests.post(f"{PRICING_URL}/pricing/calculate", json=payload, timeout=10)
    assert r.status_code == 201
    result = r.json()
    assert result.get("suggested_price") > 0
    print(f"PASO 4 OK: Precio calculado: {result['suggested_price']}")

def test_step5_integration_flow(auth_headers):
    r = requests.post(
        f"{BASE_URL}/api/integration/trigger/{BATCH_ID}",
        headers=auth_headers,
        timeout=30
    )
    assert r.status_code == 201
    result = r.json()
    assert result.get("status") == "completed"
    steps = {s["step_name"]: s["status"] for s in result.get("steps", [])}
    for step in ["inventory", "enrichment", "normalization", "catalog"]:
        assert steps.get(step) == "completed", f"Paso {step} no completado"
    print("PASO 5 OK: Flujo end-to-end completado")

def test_step6_create_order():
    payload = {
        "customer_id": "e2e-customer-001",
        "items": [
            {
                "book_id": "REF-GATSBY",
                "quantity": 1,
                "unit_price": 18900.0,
                "title": "The Great Gatsby"
            }
        ],
        "notes": "Pedido E2E Test"
    }
    r = requests.post(f"{ORDER_URL}/orders", json=payload, timeout=10)
    assert r.status_code == 201
    result = r.json()
    assert result["status"] == "pending"
    assert result["total_amount"] == 18900.0
    print(f"PASO 6 OK: Pedido creado - ID: {result['id']}")
    return result["id"]

def test_step7_order_state_machine():
    payload = {
        "customer_id": "e2e-customer-002",
        "items": [{"book_id": "REF-ORWELL", "quantity": 1, "unit_price": 15000.0, "title": "1984"}],
    }
    r = requests.post(f"{ORDER_URL}/orders", json=payload, timeout=10)
    assert r.status_code == 201
    order_id = r.json()["id"]

    r = requests.put(f"{ORDER_URL}/orders/{order_id}/status", json={"status": "confirmed"})
    assert r.status_code == 200
    assert r.json()["status"] == "confirmed"

    r = requests.put(f"{ORDER_URL}/orders/{order_id}/status", json={"status": "shipped"})
    assert r.status_code == 200
    assert r.json()["status"] == "shipped"

    r = requests.put(f"{ORDER_URL}/orders/{order_id}/status", json={"status": "delivered"})
    assert r.status_code == 200
    assert r.json()["status"] == "delivered"

    print("PASO 7 OK: Maquina de estados completa pending->confirmed->shipped->delivered")
