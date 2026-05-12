"""Cart router (Sprint 3 - Dev 6 Jenn).
Gateway hacia cart-service. Todas las rutas requieren JWT.
"""
from fastapi import APIRouter, Depends, HTTPException, Request, status
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.application.auth_middleware import validate_jwt
from app.infrastructure.clients.cart_client import CartClient

router = APIRouter(prefix="/api/cart", tags=["cart"])
limiter = Limiter(key_func=get_remote_address)


@router.post("/items", status_code=201)
@limiter.limit("300/minute")
async def add_cart_item(
    request: Request,
    item: dict,
    payload: dict = Depends(validate_jwt),
):
    """Agrega un item al carrito del cliente autenticado."""
    customer_id = item.get("customer_id") or payload.get("sub") or payload.get("user_id")
    if not customer_id:
        raise HTTPException(status_code=400, detail="customer_id requerido")
    item_payload = {k: v for k, v in item.items() if k != "customer_id"}
    try:
        client = CartClient()
        token = request.headers.get("authorization", "").replace("Bearer ", "")
        return await client.add_item(customer_id, item_payload, token=token)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"cart-service unavailable: {e}")


@router.get("/{customer_id}")
@limiter.limit("300/minute")
async def get_cart(
    request: Request,
    customer_id: str,
    payload: dict = Depends(validate_jwt),
):
    """Devuelve el carrito completo del cliente."""
    try:
        client = CartClient()
        token = request.headers.get("authorization", "").replace("Bearer ", "")
        return await client.get_cart(customer_id, token=token)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"cart-service unavailable: {e}")


@router.put("/items/{item_id}")
@limiter.limit("300/minute")
async def update_cart_item(
    request: Request,
    item_id: str,
    item_data: dict,
    payload: dict = Depends(validate_jwt),
):
    """Actualiza la cantidad de un item del carrito."""
    try:
        client = CartClient()
        token = request.headers.get("authorization", "").replace("Bearer ", "")
        return await client.update_item(item_id, item_data, token=token)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"cart-service unavailable: {e}")


@router.delete("/items/{item_id}")
@limiter.limit("300/minute")
async def delete_cart_item(
    request: Request,
    item_id: str,
    payload: dict = Depends(validate_jwt),
):
    """Elimina un item del carrito."""
    try:
        client = CartClient()
        token = request.headers.get("authorization", "").replace("Bearer ", "")
        return await client.delete_item(item_id, token=token)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"cart-service unavailable: {e}")
