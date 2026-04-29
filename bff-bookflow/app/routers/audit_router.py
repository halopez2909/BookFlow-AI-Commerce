from fastapi import APIRouter, Depends, HTTPException
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
