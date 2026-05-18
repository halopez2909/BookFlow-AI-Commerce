import requests
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
