import os
import httpx
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

INVENTORY_URL = os.getenv("INVENTORY_URL", "http://inventory-service:8002")
ENRICHMENT_URL = os.getenv("ENRICHMENT_URL", "http://ai-enrichment-service:8004")
NORMALIZATION_URL = os.getenv("NORMALIZATION_URL", "http://normalization-service:8005")
CATALOG_URL = os.getenv("CATALOG_URL", "http://catalog-service:8003")
TIMEOUT = int(os.getenv("FLOW_TIMEOUT_SECONDS", "30"))


class InventoryClient:
    async def get_batch(self, batch_id: str) -> dict:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            r = await client.get(f"{INVENTORY_URL}/inventory/batches/{batch_id}")
            r.raise_for_status()
            return r.json()

    async def get_batch_items(self, batch_id: str) -> list:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            r = await client.get(f"{INVENTORY_URL}/inventory/batches/{batch_id}/summary")
            r.raise_for_status()
            return r.json()


class EnrichmentClient:
    async def enrich(self, book_reference: str, title: str, author: str, isbn: Optional[str] = None) -> dict:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            r = await client.post(f"{ENRICHMENT_URL}/enrichment/enrich", json={
                "book_reference": book_reference,
                "title": title,
                "author": author,
                "isbn": isbn,
            })
            r.raise_for_status()
            return r.json()


class NormalizationClient:
    async def normalize(self, enrichment_result_id: str, title: str, author: str, isbn: Optional[str] = None) -> dict:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            r = await client.post(f"{NORMALIZATION_URL}/normalization/normalize", json={
                "enrichment_result_id": enrichment_result_id,
                "title": title,
                "author": author,
                "isbn": isbn,
            })
            r.raise_for_status()
            return r.json()


class CatalogClient:
    async def get_categories(self) -> list:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            r = await client.get(f"{CATALOG_URL}/catalog/categories")
            r.raise_for_status()
            return r.json()

    async def register_book(self, book_data: dict) -> dict:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            r = await client.post(f"{CATALOG_URL}/catalog/books", json=book_data)
            r.raise_for_status()
            return r.json()
