from fastapi import APIRouter, Depends, HTTPException
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
