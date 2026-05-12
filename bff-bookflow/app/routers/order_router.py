"""Order router (Sprint 3 - Dev 6 Jenn).
Gateway hacia order-service. Todas las rutas requieren JWT.
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Request

from app.application.auth_middleware import validate_jwt
from app.infrastructure.clients.order_client import OrderClient
from app.routers.cart_router import limiter

router = APIRouter(prefix="/api/orders", tags=["orders"])


@router.post("", status_code=201)
@limiter.limit("300/minute")
async def create_order(
    request: Request,
    order_data: dict,
    payload: dict = Depends(validate_jwt),
):
    """Crea un nuevo pedido a partir del carrito."""
    try:
        client = OrderClient()
        token = request.headers.get("authorization", "").replace("Bearer ", "")
        return await client.create_order(order_data, token=token)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"order-service unavailable: {e}")


@router.get("/{order_id}")
@limiter.limit("300/minute")
async def get_order(
    request: Request,
    order_id: str,
    payload: dict = Depends(validate_jwt),
):
    """Devuelve un pedido por su id."""
    try:
        client = OrderClient()
        token = request.headers.get("authorization", "").replace("Bearer ", "")
        return await client.get_order(order_id, token=token)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"order not found: {e}")


@router.get("")
@limiter.limit("300/minute")
async def list_orders(
    request: Request,
    customer_id: Optional[str] = None,
    page: int = 1,
    page_size: int = 20,
    payload: dict = Depends(validate_jwt),
):
    """Lista pedidos paginados, filtrables por customer_id."""
    try:
        client = OrderClient()
        token = request.headers.get("authorization", "").replace("Bearer ", "")
        return await client.list_orders(customer_id=customer_id, page=page, page_size=page_size, token=token)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"order-service unavailable: {e}")


@router.put("/{order_id}/status")
@limiter.limit("300/minute")
async def update_order_status(
    request: Request,
    order_id: str,
    status_data: dict,
    payload: dict = Depends(validate_jwt),
):
    """Cambia el estado de un pedido (pendiente, confirmado, cancelado, etc)."""
    new_status = status_data.get("status")
    if not new_status:
        raise HTTPException(status_code=400, detail="status requerido")
    try:
        client = OrderClient()
        token = request.headers.get("authorization", "").replace("Bearer ", "")
        return await client.update_status(order_id, new_status, token=token)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"order-service unavailable: {e}")
