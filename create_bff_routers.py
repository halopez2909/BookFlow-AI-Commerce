import os

normalization_router = """from fastapi import APIRouter, Depends, HTTPException
import httpx
import os
from app.application.auth_middleware import validate_jwt

router = APIRouter(prefix="/api/normalization", tags=["normalization"])
NORMALIZATION_URL = os.getenv("NORMALIZATION_URL", "http://normalization-service:8005")

@router.post("/normalize", status_code=201)
async def normalize(data: dict, payload: dict = Depends(validate_jwt)):
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.post(f"{NORMALIZATION_URL}/normalization/normalize", json=data)
            r.raise_for_status()
            return r.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/batch", status_code=201)
async def normalize_batch(data: dict, payload: dict = Depends(validate_jwt)):
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.post(f"{NORMALIZATION_URL}/normalization/batch", json=data)
            r.raise_for_status()
            return r.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/records")
async def get_records(payload: dict = Depends(validate_jwt)):
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(f"{NORMALIZATION_URL}/normalization/records")
            r.raise_for_status()
            return r.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
"""

pricing_router = """from fastapi import APIRouter, Depends, HTTPException
import httpx
import os
from app.application.auth_middleware import validate_jwt

router = APIRouter(prefix="/api/pricing", tags=["pricing"])
PRICING_URL = os.getenv("PRICING_URL", "http://pricing-service:8006")

@router.post("/calculate", status_code=201)
async def calculate_price(data: dict, payload: dict = Depends(validate_jwt)):
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.post(f"{PRICING_URL}/pricing/calculate", json=data)
            r.raise_for_status()
            return r.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/decisions/{book_reference}")
async def get_pricing_decision(book_reference: str, payload: dict = Depends(validate_jwt)):
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(f"{PRICING_URL}/pricing/decisions/{book_reference}")
            r.raise_for_status()
            return r.json()
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
"""

audit_router = """from fastapi import APIRouter, Depends, HTTPException
import httpx
import os
from app.application.auth_middleware import validate_jwt

router = APIRouter(prefix="/api/audit", tags=["audit"])
AUDIT_URL = os.getenv("AUDIT_URL", "http://audit-service:8007")

@router.get("/summary/{book_reference}")
async def get_audit_summary(book_reference: str, payload: dict = Depends(validate_jwt)):
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(f"{AUDIT_URL}/audit/summary/{book_reference}")
            r.raise_for_status()
            return r.json()
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/pricing/{book_reference}")
async def get_pricing_audit(book_reference: str, payload: dict = Depends(validate_jwt)):
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(f"{AUDIT_URL}/audit/pricing/{book_reference}")
            r.raise_for_status()
            return r.json()
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/enrichment/{book_reference}")
async def get_enrichment_audit(book_reference: str, payload: dict = Depends(validate_jwt)):
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(f"{AUDIT_URL}/audit/enrichment/{book_reference}")
            r.raise_for_status()
            return r.json()
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
"""

integration_router = """from fastapi import APIRouter, Depends, HTTPException
import httpx
import os
from app.application.auth_middleware import validate_jwt

router = APIRouter(prefix="/api/integration", tags=["integration"])
INTEGRATION_URL = os.getenv("INTEGRATION_URL", "http://integration-service:8006")

@router.post("/trigger/{batch_id}", status_code=201)
async def trigger_integration(batch_id: str, payload: dict = Depends(validate_jwt)):
    try:
        async with httpx.AsyncClient(timeout=60) as client:
            r = await client.post(f"{INTEGRATION_URL}/integration/trigger/{batch_id}")
            r.raise_for_status()
            return r.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status/{batch_id}")
async def get_integration_status(batch_id: str, payload: dict = Depends(validate_jwt)):
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(f"{INTEGRATION_URL}/integration/status/{batch_id}")
            r.raise_for_status()
            return r.json()
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/external/health")
async def external_health():
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            r = await client.get(f"{INTEGRATION_URL}/health")
            r.raise_for_status()
            return r.json()
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))
"""

system_router = """from fastapi import APIRouter
import httpx
import os

router = APIRouter(prefix="/api/system", tags=["system"])

SERVICES = {
    "auth-service": os.getenv("AUTH_URL", "http://auth-service:8001"),
    "inventory-service": os.getenv("INVENTORY_URL", "http://inventory-service:8002"),
    "catalog-service": os.getenv("CATALOG_URL", "http://catalog-service:8003"),
    "ai-enrichment-service": os.getenv("ENRICHMENT_URL", "http://ai-enrichment-service:8004"),
    "normalization-service": os.getenv("NORMALIZATION_URL", "http://normalization-service:8005"),
    "integration-service": os.getenv("INTEGRATION_URL", "http://integration-service:8006"),
    "audit-service": os.getenv("AUDIT_URL", "http://audit-service:8007"),
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
"""

files = {
    'bff-bookflow/app/routers/normalization_router.py': normalization_router,
    'bff-bookflow/app/routers/pricing_router.py': pricing_router,
    'bff-bookflow/app/routers/audit_router.py': audit_router,
    'bff-bookflow/app/routers/integration_router.py': integration_router,
    'bff-bookflow/app/routers/system_router.py': system_router,
}

for path, content in files.items():
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Created: {path}')

# Update .env
env_content = """AUTH_URL=http://auth-service:8001
INVENTORY_URL=http://inventory-service:8002
CATALOG_URL=http://catalog-service:8003
ENRICHMENT_URL=http://ai-enrichment-service:8004
NORMALIZATION_URL=http://normalization-service:8005
INTEGRATION_URL=http://integration-service:8006
AUDIT_URL=http://audit-service:8007
JWT_SECRET_KEY=supersecretkey123bookflow
JWT_ALGORITHM=HS256
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173,http://localhost:5174
"""
with open('bff-bookflow/.env', 'w', encoding='utf-8') as f:
    f.write(env_content)
print('Updated: bff-bookflow/.env')
print('All done!')
