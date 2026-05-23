from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
import httpx
import os
from app.application.auth_middleware import validate_jwt

router = APIRouter(prefix="/api/orders", tags=["orders"])
ORDER_URL = os.getenv("ORDER_URL", "http://order-service:8010")

@router.post("", status_code=201)
async def create_order(data: dict, payload: dict = Depends(validate_jwt)):
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.post(f"{ORDER_URL}/orders", json=data)
            if r.status_code == 409:
                raise HTTPException(status_code=409, detail=r.json().get("detail"))
            if r.status_code == 400:
                raise HTTPException(status_code=400, detail=r.json().get("detail"))
            r.raise_for_status()
            return r.json()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("")
async def get_orders(customer_id: Optional[str] = None, payload: dict = Depends(validate_jwt)):
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            params = {"customer_id": customer_id} if customer_id else {}
            r = await client.get(f"{ORDER_URL}/orders", params=params)
            r.raise_for_status()
            return r.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{order_id}")
async def get_order(order_id: str, payload: dict = Depends(validate_jwt)):
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(f"{ORDER_URL}/orders/{order_id}")
            r.raise_for_status()
            return r.json()
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/{order_id}/status")
async def update_order_status(order_id: str, data: dict, payload: dict = Depends(validate_jwt)):
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.put(f"{ORDER_URL}/orders/{order_id}/status", json=data)
            r.raise_for_status()
            return r.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
