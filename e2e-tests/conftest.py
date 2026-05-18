import pytest
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
