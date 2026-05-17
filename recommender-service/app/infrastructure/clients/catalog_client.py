# app/infrastructure/clients/catalog_client.py
import httpx
import os
from app.domain.models import Book

CATALOG_URL = os.getenv("CATALOG_URL", "http://catalog-service:8000")

class CatalogClient:
    def get_book(self, book_id: str) -> Book | None:
        response = httpx.get(f"{CATALOG_URL}/books/{book_id}")
        if response.status_code == 200:
            return Book(**response.json())
        return None

    def get_by_category(self, category: str) -> list[Book]:
        response = httpx.get(f"{CATALOG_URL}/books?category={category}")
        return [Book(**b) for b in response.json()] if response.status_code == 200 else []

    def get_by_author(self, author: str) -> list[Book]:
        response = httpx.get(f"{CATALOG_URL}/books?author={author}")
        return [Book(**b) for b in response.json()] if response.status_code == 200 else []

    def get_by_price_range(self, min_price: float, max_price: float) -> list[Book]:
        response = httpx.get(f"{CATALOG_URL}/books?min_price={min_price}&max_price={max_price}")
        return [Book(**b) for b in response.json()] if response.status_code == 200 else []
        
    def get_popular(self) -> list[Book]:
        # Idealmente esto lee de los logs o un endpoint específico del catálogo
        response = httpx.get(f"{CATALOG_URL}/books/popular")
        return [Book(**b) for b in response.json()] if response.status_code == 200 else []