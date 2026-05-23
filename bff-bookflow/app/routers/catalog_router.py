import httpx
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from app.infrastructure.clients.catalog_client import CatalogClient
from app.application.auth_middleware import validate_jwt

router = APIRouter(prefix="/api/catalog", tags=["catalog"])

@router.get("/books")
async def get_books(
    title: Optional[str] = None,
    author: Optional[str] = None,
    category_id: Optional[str] = None,
    page: int = 1,
    page_size: int = 20,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    available: Optional[bool] = None,
):
    try:
        client = CatalogClient()
        return await client.get_books(title, author, category_id, page, page_size, min_price, max_price, available)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/books/{book_id}")
async def get_book(book_id: str):
    try:
        client = CatalogClient()
        return await client.get_book_by_id(book_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail="Book not found")

@router.get("/categories")
async def get_categories():
    try:
        client = CatalogClient()
        return await client.get_categories()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/books", status_code=201)
async def create_book(book_data: dict, payload: dict = Depends(validate_jwt)):
    try:
        client = CatalogClient()
        return await client.create_book(book_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/categories", status_code=201)
async def create_category(category_data: dict, payload: dict = Depends(validate_jwt)):
    try:
        client = CatalogClient()
        return await client.create_category(category_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/books/{book_id}/full")
async def get_book_full(book_id: str):
    import asyncio
    import os
    CATALOG_URL = os.getenv("CATALOG_URL", "http://catalog-service:8003")
    RECOMMENDER_URL = os.getenv("RECOMMENDER_URL", "http://recommender-service:8090")
    PRICING_URL = os.getenv("PRICING_URL", "http://pricing-service:8008")

    async def fetch(client, url):
        try:
            r = await client.get(url, timeout=10)
            return r.json() if r.status_code == 200 else None
        except Exception:
            return None

    async with httpx.AsyncClient() as client:
        book, recommendations, pricing = await asyncio.gather(
            fetch(client, f"{CATALOG_URL}/catalog/books/{book_id}"),
            fetch(client, f"{RECOMMENDER_URL}/recommendations/{book_id}"),
            fetch(client, f"{PRICING_URL}/pricing/decisions/{book_id}"),
        )

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    return {
        "book": book,
        "recommendations": recommendations or [],
        "pricing": pricing,
    }
