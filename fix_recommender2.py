catalog_client = """import httpx
import os
from typing import List, Optional
from app.domain.models import Book

CATALOG_URL = os.getenv("CATALOG_URL", "http://catalog-service:8003")

class CatalogClient:
    async def get_book(self, book_id: str) -> Optional[Book]:
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                r = await client.get(f"{CATALOG_URL}/catalog/books/{book_id}")
                if r.status_code == 200:
                    data = r.json()
                    return Book(
                        id=str(data.get("id", "")),
                        title=data.get("title", ""),
                        author=data.get("author", ""),
                        category=data.get("category_id", ""),
                        price=float(data.get("suggested_price") or 0.0),
                        published_flag=data.get("published_flag", True),
                        quantity_available=1,
                    )
        except Exception:
            pass
        return None

    async def get_catalog(self) -> List[Book]:
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                r = await client.get(f"{CATALOG_URL}/catalog/books", params={"page_size": 50})
                if r.status_code == 200:
                    items = r.json().get("items", [])
                    books = []
                    for data in items:
                        books.append(Book(
                            id=str(data.get("id", "")),
                            title=data.get("title", ""),
                            author=data.get("author", ""),
                            category=data.get("category_id", ""),
                            price=float(data.get("suggested_price") or 0.0),
                            published_flag=data.get("published_flag", True),
                            quantity_available=1,
                        ))
                    return books
        except Exception:
            pass
        return []

    async def get_by_category(self, category: str) -> List[Book]:
        return await self.get_catalog()

    async def get_by_author(self, author: str) -> List[Book]:
        return await self.get_catalog()

    async def get_by_price_range(self, min_price: float, max_price: float) -> List[Book]:
        return await self.get_catalog()
"""

with open("recommender-service/app/infrastructure/clients/catalog_client.py", "w", encoding="utf-8") as f:
    f.write(catalog_client)
print("Done")
