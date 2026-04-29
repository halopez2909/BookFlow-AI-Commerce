from fastapi import APIRouter, Depends, HTTPException
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
