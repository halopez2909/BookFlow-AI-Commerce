"""Recommender router (Sprint 3 - Dev 6 Jenn).
Gateway hacia recommender-service. Rutas PUBLICAS (sin JWT).
"""
from fastapi import APIRouter, HTTPException, Request
from app.infrastructure.clients.recommender_client import RecommenderClient
from app.routers.cart_router import limiter

router = APIRouter(prefix="/api/recommendations", tags=["recommendations"])


@router.get("/popular")
@limiter.limit("100/minute")
async def popular_recommendations(request: Request, limit: int = 10):
    """Top N libros populares de la plataforma."""
    try:
        client = RecommenderClient()
        return await client.get_popular(limit=limit)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"recommender-service unavailable: {e}")


@router.get("/{book_id}")
@limiter.limit("100/minute")
async def recommendations_for_book(request: Request, book_id: str, limit: int = 6):
    """Recomendaciones por libro (similares)."""
    try:
        client = RecommenderClient()
        return await client.get_recommendations(book_id, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"recommender-service unavailable: {e}")
