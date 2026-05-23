from fastapi import APIRouter, Depends, HTTPException
import httpx
import os
from app.application.auth_middleware import validate_jwt

router = APIRouter(prefix="/api/cart", tags=["cart"])
CART_URL = os.getenv("CART_URL", "http://cart-service:8011")

@router.post("/items", status_code=201)
async def add_to_cart(data: dict):
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.post(f"{CART_URL}/cart/items", json=data)
            r.raise_for_status()
            return r.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{customer_id}")
async def get_cart(customer_id: str):
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(f"{CART_URL}/cart/{customer_id}")
            r.raise_for_status()
            return r.json()
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/items/{item_id}")
async def update_cart_item(item_id: int, data: dict):
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.put(f"{CART_URL}/cart/items/{item_id}", json=data)
            r.raise_for_status()
            return r.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/items/{item_id}")
async def remove_cart_item(item_id: int):
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.delete(f"{CART_URL}/cart/items/{item_id}")
            r.raise_for_status()
            return r.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{customer_id}")
async def clear_cart(customer_id: str):
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.delete(f"{CART_URL}/cart/{customer_id}")
            r.raise_for_status()
            return r.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
