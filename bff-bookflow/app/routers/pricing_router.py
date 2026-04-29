from fastapi import APIRouter, Depends, HTTPException
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
