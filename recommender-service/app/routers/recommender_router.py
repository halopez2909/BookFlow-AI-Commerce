from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional
from app.domain.models import Book
from app.application.use_cases import GetRecommendationsUseCase, GetPopularBooksUseCase
from app.infrastructure.clients.catalog_client import CatalogClient
from app.infrastructure.clients.inventory_client import InventoryClient

router = APIRouter(prefix="/recommendations", tags=["Recommendations Engine"])

# Instanciamos los adaptadores de infraestructura una sola vez
catalog_client = CatalogClient()
inventory_client = InventoryClient()

@router.get("/popular", response_model=List[Book])
async def get_popular_books():
    """Retorna los 10 libros más consultados de la semana."""
    try:
        use_case = GetPopularBooksUseCase(catalog_client)
        return await use_case.execute(limit=10)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{book_id}", response_model=List[Book])
async def get_book_recommendations(
    book_id: str,
    strategy: Optional[str] = Query(None, description="Estrategias: category, author, price")
):
    """Retorna hasta 6 recomendaciones basadas en el book_id y la estrategia elegida."""
    try:
        use_case = GetRecommendationsUseCase(catalog_client, inventory_client)
        return await use_case.execute(book_id=book_id, strategy_name=strategy, limit=6)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))