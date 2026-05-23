import os

BASE = "e2e-tests"
os.makedirs(BASE, exist_ok=True)

files = {}

files["requirements.txt"] = """pytest==8.2.0
pytest-asyncio==0.23.6
httpx==0.27.0
requests==2.31.0
"""

files["conftest.py"] = """import pytest
import requests

BASE_URL = "http://localhost:8000"
AUTH_URL = "http://localhost:8001"
INVENTORY_URL = "http://localhost:8002"
CATALOG_URL = "http://localhost:8003"
ENRICHMENT_URL = "http://localhost:8004"
NORMALIZATION_URL = "http://localhost:8005"
INTEGRATION_URL = "http://localhost:8006"
AUDIT_URL = "http://localhost:8007"
PRICING_URL = "http://localhost:8008"
EXTERNAL_URL = "http://localhost:8009"
ORDER_URL = "http://localhost:8010"

@pytest.fixture(scope="session")
def auth_token():
    r = requests.post(f"{BASE_URL}/api/auth/login", json={"email": "admin@bookflow.com", "password": "admin1234"})
    assert r.status_code == 200, f"Login failed: {r.text}"
    return r.json()["access_token"]

@pytest.fixture(scope="session")
def auth_headers(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}
"""

files["tests/__init__.py"] = ""

files["tests/test_health.py"] = """import requests
import pytest

SERVICES = [
    ("auth-service",          "http://localhost:8001/health"),
    ("inventory-service",     "http://localhost:8002/health"),
    ("catalog-service",       "http://localhost:8003/health"),
    ("ai-enrichment-service", "http://localhost:8004/health"),
    ("normalization-service", "http://localhost:8005/health"),
    ("integration-service",   "http://localhost:8006/health"),
    ("audit-service",         "http://localhost:8007/health"),
    ("pricing-service",       "http://localhost:8008/health"),
    ("external-service",      "http://localhost:8009/health"),
    ("order-service",         "http://localhost:8010/health"),
    ("bff-health",            "http://localhost:8000/api/system/health"),
]

@pytest.mark.parametrize("name,url", SERVICES)
def test_service_health(name, url):
    r = requests.get(url, timeout=10)
    assert r.status_code == 200, f"{name} no responde: {r.status_code}"
    data = r.json()
    if "status" in data:
        assert data["status"] in ["ok", "healthy"], f"{name} status: {data['status']}"
    print(f"OK: {name}")

def test_bff_overall_health():
    r = requests.get("http://localhost:8000/api/system/health", timeout=15)
    assert r.status_code == 200
    data = r.json()
    assert data.get("overall") == "ok", f"Sistema degradado: {data}"
"""

files["tests/test_full_flow.py"] = """import requests
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
"""

files["tests/test_error_scenarios.py"] = """import requests
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
"""

files["health_check.py"] = """import requests

SERVICES = [
    ("auth-service",          "http://localhost:8001/health"),
    ("inventory-service",     "http://localhost:8002/health"),
    ("catalog-service",       "http://localhost:8003/health"),
    ("ai-enrichment-service", "http://localhost:8004/health"),
    ("normalization-service", "http://localhost:8005/health"),
    ("integration-service",   "http://localhost:8006/health"),
    ("audit-service",         "http://localhost:8007/health"),
    ("pricing-service",       "http://localhost:8008/health"),
    ("external-service",      "http://localhost:8009/health"),
    ("order-service",         "http://localhost:8010/health"),
    ("bff-bookflow",          "http://localhost:8000/health"),
]

print("\\n" + "="*60)
print("BOOKFLOW AI COMMERCE - HEALTH CHECK")
print("="*60)

all_ok = True
for name, url in SERVICES:
    try:
        r = requests.get(url, timeout=5)
        status = "OK" if r.status_code == 200 else "ERROR"
        latency = r.elapsed.total_seconds() * 1000
        print(f"  {status:5} | {name:30} | {latency:.0f}ms")
        if r.status_code != 200:
            all_ok = False
    except Exception as e:
        print(f"  DOWN  | {name:30} | {str(e)[:30]}")
        all_ok = False

print("="*60)
print(f"RESULTADO: {'TODO OK' if all_ok else 'HAY SERVICIOS CAIDOS'}")
print("="*60)
"""

files["run_e2e.sh"] = """#!/bin/bash
echo "============================================"
echo "BOOKFLOW AI COMMERCE - E2E TEST SUITE"
echo "============================================"

echo ""
echo "1. Verificando health de todos los servicios..."
python health_check.py

echo ""
echo "2. Ejecutando pruebas E2E..."
pytest tests/ -v --tb=short

echo ""
echo "============================================"
echo "E2E TESTS COMPLETADOS"
echo "============================================"
"""

for path, content in files.items():
    full_path = os.path.join(BASE, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"OK: {path}")

print("\nE2E Tests creados!")
