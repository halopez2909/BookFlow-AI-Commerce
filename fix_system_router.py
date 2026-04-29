content = '''import os
import httpx
from fastapi import APIRouter

router = APIRouter(prefix="/api/system", tags=["system"])

SERVICES = {
    "auth-service": os.getenv("AUTH_URL", "http://auth-service:8001"),
    "inventory-service": os.getenv("INVENTORY_URL", "http://inventory-service:8002"),
    "catalog-service": os.getenv("CATALOG_URL", "http://catalog-service:8003"),
    "ai-enrichment-service": os.getenv("ENRICHMENT_URL", "http://ai-enrichment-service:8004"),
    "normalization-service": os.getenv("NORMALIZATION_URL", "http://normalization-service:8005"),
    "integration-service": os.getenv("INTEGRATION_URL", "http://integration-service:8006"),
    "audit-service": os.getenv("AUDIT_URL", "http://audit-service:8007"),
    "pricing-service": os.getenv("PRICING_URL", "http://pricing-service:8008"),
    "external-service": os.getenv("EXTERNAL_URL", "http://external-service:8009"),
}


@router.get("/health")
async def system_health():
    results = {}
    for name, url in SERVICES.items():
        try:
            async with httpx.AsyncClient(timeout=3) as client:
                r = await client.get(f"{url}/health")
                results[name] = {"status": "ok", "code": r.status_code}
        except Exception as e:
            results[name] = {"status": "error", "detail": str(e)}
    overall = "ok" if all(v["status"] == "ok" for v in results.values()) else "degraded"
    return {"overall": overall, "services": results}
'''
with open('bff-bookflow/app/routers/system_router.py', 'w', encoding='utf-8') as f:
    f.write(content)

# Update BFF .env with new services
env = open('bff-bookflow/.env', 'r', encoding='utf-8').read()
if 'PRICING_URL' not in env:
    env += '\nPRICING_URL=http://pricing-service:8008'
if 'EXTERNAL_URL' not in env:
    env += '\nEXTERNAL_URL=http://external-service:8009'
with open('bff-bookflow/.env', 'w', encoding='utf-8') as f:
    f.write(env)
print('system_router and .env updated!')
