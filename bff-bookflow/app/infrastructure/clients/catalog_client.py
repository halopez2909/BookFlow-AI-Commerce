import os
import httpx
from dotenv import load_dotenv

load_dotenv()

CATALOG_URL = os.getenv("CATALOG_URL")


class CatalogClient:

    async def get_books(self, title: str = None, author: str = None, category_id: str = None, page: int = 1, page_size: int = 20) -> dict:
        async with httpx.AsyncClient() as client:
            params = {"page": page, "page_size": page_size}
            if title:
                params["title"] = title
            if author:
                params["author"] = author
            if category_id:
                params["category_id"] = category_id
            response = await client.get(f"{CATALOG_URL}/catalog/books", params=params)
            response.raise_for_status()
            return response.json()

    async def get_book_by_id(self, book_id: str) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{CATALOG_URL}/catalog/books/{book_id}")
            response.raise_for_status()
            return response.json()

    async def get_categories(self) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{CATALOG_URL}/catalog/categories")
            response.raise_for_status()
            return response.json()

    async def create_book(self, book_data: dict) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{CATALOG_URL}/catalog/books", json=book_data)
            response.raise_for_status()
            return response.json()

    async def create_category(self, category_data: dict) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{CATALOG_URL}/catalog/categories", json=category_data)
            response.raise_for_status()
            return response.json()
