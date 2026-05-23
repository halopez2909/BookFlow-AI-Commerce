from fastapi import APIRouter
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
