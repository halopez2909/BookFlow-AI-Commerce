import os

# 1. Update requirements to add slowapi
reqs = open("bff-bookflow/requirements.txt", "r", encoding="utf-8").read()
if "slowapi" not in reqs:
    with open("bff-bookflow/requirements.txt", "a", encoding="utf-8") as f:
        f.write("\nslowapi==0.1.9\n")
    print("slowapi agregado a requirements")

# 2. Update system_router with all services including Sprint 3
system_router = """from fastapi import APIRouter
import httpx
import os
import asyncio

router = APIRouter(prefix="/api/system", tags=["system"])

SERVICES = {
    "auth-service":          os.getenv("AUTH_URL", "http://auth-service:8001"),
    "inventory-service":     os.getenv("INVENTORY_URL", "http://inventory-service:8002"),
    "catalog-service":       os.getenv("CATALOG_URL", "http://catalog-service:8003"),
    "ai-enrichment-service": os.getenv("ENRICHMENT_URL", "http://ai-enrichment-service:8004"),
    "normalization-service": os.getenv("NORMALIZATION_URL", "http://normalization-service:8005"),
    "integration-service":   os.getenv("INTEGRATION_URL", "http://integration-service:8006"),
    "audit-service":         os.getenv("AUDIT_URL", "http://audit-service:8007"),
    "pricing-service":       os.getenv("PRICING_URL", "http://pricing-service:8008"),
    "external-service":      os.getenv("EXTERNAL_URL", "http://external-service:8009"),
    "order-service":         os.getenv("ORDER_URL", "http://order-service:8010"),
    "cart-service":          os.getenv("CART_URL", "http://cart-service:8011"),
    "ai-assistant-service":  os.getenv("ASSISTANT_URL", "http://ai-assistant-service:8012"),
    "recommender-service":   os.getenv("RECOMMENDER_URL", "http://recommender-service:8090"),
}

async def check_service(name: str, base_url: str) -> dict:
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            r = await client.get(f"{base_url}/health")
            return {"status": "ok", "code": r.status_code}
    except Exception as e:
        return {"status": "down", "error": str(e)[:50]}

@router.get("/health")
async def system_health():
    tasks = {name: check_service(name, url) for name, url in SERVICES.items()}
    results = await asyncio.gather(*tasks.values())
    services = dict(zip(tasks.keys(), results))
    overall = "ok" if all(s["status"] == "ok" for s in services.values()) else "degraded"
    return {"overall": overall, "services": services}
"""

with open("bff-bookflow/app/routers/system_router.py", "w", encoding="utf-8") as f:
    f.write(system_router)
print("system_router.py actualizado con Sprint 3")

# 3. Add /api/books/{id}/full endpoint to catalog_router
catalog_router = open("bff-bookflow/app/routers/catalog_router.py", "r", encoding="utf-8").read()
if "/full" not in catalog_router:
    full_endpoint = """
@router.get("/books/{book_id}/full")
async def get_book_full(book_id: str):
    import asyncio
    import os
    CATALOG_URL = os.getenv("CATALOG_URL", "http://catalog-service:8003")
    RECOMMENDER_URL = os.getenv("RECOMMENDER_URL", "http://recommender-service:8090")
    PRICING_URL = os.getenv("PRICING_URL", "http://pricing-service:8008")

    async def fetch(client, url):
        try:
            r = await client.get(url, timeout=10)
            return r.json() if r.status_code == 200 else None
        except Exception:
            return None

    async with httpx.AsyncClient() as client:
        book, recommendations, pricing = await asyncio.gather(
            fetch(client, f"{CATALOG_URL}/catalog/books/{book_id}"),
            fetch(client, f"{RECOMMENDER_URL}/recommendations/{book_id}"),
            fetch(client, f"{PRICING_URL}/pricing/decisions/{book_id}"),
        )

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    return {
        "book": book,
        "recommendations": recommendations or [],
        "pricing": pricing,
    }
"""
    # Add import httpx if not present
    if "import httpx" not in catalog_router:
        catalog_router = "import httpx\n" + catalog_router
    catalog_router += full_endpoint
    with open("bff-bookflow/app/routers/catalog_router.py", "w", encoding="utf-8") as f:
        f.write(catalog_router)
    print("catalog_router.py actualizado con /books/{id}/full")

# 4. Update main.py with rate limiting
main_py = """import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from dotenv import load_dotenv
from app.routers.auth_router import router as auth_router
from app.routers.inventory_router import router as inventory_router
from app.routers.catalog_router import router as catalog_router
from app.routers.config_router import router as config_router
from app.routers.normalization_router import router as normalization_router
from app.routers.pricing_router import router as pricing_router
from app.routers.audit_router import router as audit_router
from app.routers.integration_router import router as integration_router
from app.routers.system_router import router as system_router
from app.routers.cart_router import router as cart_router
from app.routers.orders_router import router as orders_router
from app.routers.assistant_router import router as assistant_router
from app.routers.recommendations_router import router as recommendations_router

load_dotenv()

limiter = Limiter(key_func=get_remote_address, default_limits=["200/minute"])
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:5173,http://localhost:5174").split(",")

app = FastAPI(title="BFF BookFlow", version="3.0.0")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(inventory_router)
app.include_router(catalog_router)
app.include_router(config_router)
app.include_router(normalization_router)
app.include_router(pricing_router)
app.include_router(audit_router)
app.include_router(integration_router)
app.include_router(system_router)
app.include_router(cart_router)
app.include_router(orders_router)
app.include_router(assistant_router)
app.include_router(recommendations_router)

@app.get("/health")
def health():
    return {"status": "ok", "service": "bff-bookflow"}
"""

with open("bff-bookflow/main.py", "w", encoding="utf-8") as f:
    f.write(main_py)
print("main.py actualizado con rate limiting")
