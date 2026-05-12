"""Books-Full router (Sprint 3 - Dev 6 Jenn).
Facade Pattern: una sola llamada agrega catalogo + pricing + inventario + recomendaciones.
Parallel Execution con asyncio.gather.
"""
import asyncio
from fastapi import APIRouter, HTTPException, Request
from app.infrastructure.clients.catalog_client import CatalogClient
from app.infrastructure.clients.pricing_client import PricingClient
from app.infrastructure.clients.inventory_client import InventoryClient
from app.infrastructure.clients.recommender_client import RecommenderClient
from app.routers.cart_router import limiter

router = APIRouter(prefix="/api/books", tags=["books-full"])


async def _safe_call(coro, fallback):
    """Si un servicio falla, devolvemos fallback en vez de tumbar todo el endpoint."""
    try:
        return await coro
    except Exception as e:
        return {"_error": True, "detail": str(e), **fallback}


@router.get("/{book_id}/full")
@limiter.limit("100/minute")
async def get_book_full(request: Request, book_id: str):
    """Ficha completa de un libro: catalogo + pricing + stock + 6 recomendaciones.
    Las 4 llamadas se ejecutan en paralelo con asyncio.gather.
    """
    catalog = CatalogClient()
    pricing = PricingClient()
    inventory = InventoryClient()
    recommender = RecommenderClient()

    catalog_task = _safe_call(catalog.get_book_by_id(book_id), {"id": book_id})
    pricing_task = _safe_call(pricing.get_decision(book_id), {"book_id": book_id, "suggested_price": None})
    inventory_task = _safe_call(inventory.get_stock(book_id), {"book_id": book_id, "available": False, "stock": 0})
    recs_task = _safe_call(recommender.get_recommendations(book_id, limit=6), {"items": []})

    catalog_data, pricing_data, inventory_data, recs_data = await asyncio.gather(
        catalog_task, pricing_task, inventory_task, recs_task
    )

    if catalog_data.get("_error") and not catalog_data.get("title"):
        raise HTTPException(status_code=404, detail=f"Libro {book_id} no encontrado en catalogo")

    return {
        "book_id": book_id,
        "catalog": catalog_data,
        "pricing": pricing_data,
        "inventory": inventory_data,
        "recommendations": recs_data,
    }
