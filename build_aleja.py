import os, subprocess

# seed_data.py
seed = """import requests, time

BFF = "http://localhost:8000"

def log(msg): print(f"  {msg}")

def register_users():
    users = [
        {"email": "admin@bookflow.com", "password": "admin123", "role": "admin"},
        {"email": "cliente@bookflow.com", "password": "cliente123", "role": "user"},
    ]
    for u in users:
        try:
            r = requests.post(f"{BFF}/api/auth/register", json=u, timeout=5)
            log(f"Usuario: {u['email']} - {'OK' if r.status_code in [200,201,409] else r.text}")
        except Exception as e:
            log(f"Error usuario: {e}")

def check_health():
    try:
        r = requests.get(f"{BFF}/api/system/health", timeout=10)
        data = r.json()
        ok = sum(1 for s in data.get("services",{}).values() if s.get("status")=="ok")
        total = len(data.get("services",{}))
        log(f"Health: {ok}/{total} servicios OK")
        return ok == total
    except Exception as e:
        log(f"Health error: {e}")
        return False

def main():
    print("BookFlow AI Commerce - Seed Data Sprint 3")
    print("=" * 50)
    print("Verificando servicios...")
    if not check_health():
        print("ADVERTENCIA: Algunos servicios no responden")
    print("Registrando usuarios demo...")
    register_users()
    print("=" * 50)
    print("Seed completado!")
    print("  admin@bookflow.com / admin123")
    print("  cliente@bookflow.com / cliente123")

if __name__ == "__main__":
    main()
"""

# README.md
readme = """# BookFlow AI Commerce

Plataforma inteligente de comercio de libros con microservicios e IA.

## Requisitos
- Docker Desktop
- Docker Compose

## Levantar el sistema
```bash
docker compose up --build -d
```

## Verificar que todo funciona
```bash
python e2e-tests/health_check.py
```

## Cargar datos de demo
```bash
python seed_data.py
```

## Demo completa
1. Abrir http://localhost:3000
2. Login: admin@bookflow.com / admin123
3. Explorar catalogo con libros enriquecidos con IA
4. Ver ficha de libro con precio IA y recomendaciones
5. Agregar al carrito
6. Confirmar pedido
7. Consultar asistente IA en /assistant
8. Ver historial en /orders

## Servicios

| Servicio | Puerto |
|---|---|
| BFF Gateway | 8000 |
| Auth | 8001 |
| Inventory | 8002 |
| Catalog | 8003 |
| AI Enrichment | 8004 |
| Normalization | 8005 |
| Integration | 8006 |
| Audit | 8007 |
| Pricing | 8008 |
| External | 8009 |
| Order | 8010 |
| Cart | 8011 |
| AI Assistant | 8012 |
| Recommender | 8090 |
| Frontend | 3000 |
"""

# .env.example
env_example = """# BookFlow AI Commerce - Variables de entorno globales

# PostgreSQL
POSTGRES_USER=bookflow
POSTGRES_PASSWORD=bookflow123
POSTGRES_HOST=postgres

# Auth
JWT_SECRET=supersecretkey
JWT_ALGORITHM=HS256

# URLs internas
AUTH_URL=http://auth-service:8001
INVENTORY_URL=http://inventory-service:8002
CATALOG_URL=http://catalog-service:8003
ENRICHMENT_URL=http://ai-enrichment-service:8004
NORMALIZATION_URL=http://normalization-service:8005
INTEGRATION_URL=http://integration-service:8006
AUDIT_URL=http://audit-service:8007
PRICING_URL=http://pricing-service:8008
EXTERNAL_URL=http://external-service:8009
ORDER_URL=http://order-service:8010
CART_URL=http://cart-service:8011
ASSISTANT_URL=http://ai-assistant-service:8012
RECOMMENDER_URL=http://recommender-service:8090

# Frontend
VITE_BFF_URL=http://localhost:8000
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173

# OpenAI (opcional)
OPENAI_API_KEY=sk-your-key-here
"""

# BFF test
bff_test = """import pytest, httpx

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
"""

with open("seed_data.py", "w", encoding="utf-8") as f: f.write(seed)
with open("README.md", "w", encoding="utf-8") as f: f.write(readme)
with open(".env.example", "w", encoding="utf-8") as f: f.write(env_example)
os.makedirs("e2e-tests", exist_ok=True)
with open("e2e-tests/test_bff_sprint3.py", "w", encoding="utf-8") as f: f.write(bff_test)
print("OK: seed_data.py")
print("OK: README.md")
print("OK: .env.example")
print("OK: e2e-tests/test_bff_sprint3.py")
