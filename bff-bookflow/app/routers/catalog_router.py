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
):
    try:
        client = CatalogClient()
        return await client.get_books(title, author, category_id, page, page_size)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/books/{book_id}")
async def get_book(book_id: str):
    try:
        client = CatalogClient()
        return await client.get_book_by_id(book_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@router.get("/categories")
async def get_categories():
    try:
        client = CatalogClient()
        return await client.get_categories()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/books", status_code=status.HTTP_201_CREATED)
async def create_book(
    book_data: dict,
    payload: dict = Depends(validate_jwt),
):
    try:
        client = CatalogClient()
        return await client.create_book(book_data)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/categories", status_code=status.HTTP_201_CREATED)
async def create_category(
    category_data: dict,
    payload: dict = Depends(validate_jwt),
):
    try:
        client = CatalogClient()
        return await client.create_category(category_data)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
