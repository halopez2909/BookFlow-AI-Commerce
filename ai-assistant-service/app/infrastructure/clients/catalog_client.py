"""
CatalogClient: Adapter del Catalog Service. Traduce las respuestas
del catálogo a BookSnapshot (la vista que el dominio entiende).
"""
import os
from typing import List

from app.domain.entities import BookSnapshot
from app.infrastructure.clients.base_client import BaseHttpClient


class CatalogClient(BaseHttpClient):
    def __init__(self, base_url: str | None = None, timeout: float | None = None) -> None:
        super().__init__(
            base_url=base_url or os.getenv("CATALOG_URL", "http://catalog-service:8003"),
            timeout=timeout,
        )

    # ---- helpers de mapeo ----

    @staticmethod
    def _to_snapshot(raw: dict) -> BookSnapshot:
        return BookSnapshot(
            book_id=str(raw.get("id", "")),
            title=raw.get("title"),
            author=raw.get("author"),
            description=raw.get("description"),
            category=str(raw.get("category_id")) if raw.get("category_id") else None,
            price=raw.get("suggested_price"),
        )

    # ---- métodos públicos ----

    async def get_by_id(self, book_id: str) -> BookSnapshot | None:
        raw = await self._get(f"/catalog/books/{book_id}")
        if not raw:
            return None
        return self._to_snapshot(raw)

    async def search_by_title(self, title: str, limit: int = 5) -> List[BookSnapshot]:
        data = await self._get("/catalog/books", params={
            "title": title,
            "page": 1,
            "page_size": limit,
        })
        if not data:
            return []
        items = data.get("items", []) if isinstance(data, dict) else []
        return [self._to_snapshot(b) for b in items]

    async def search_by_author(self, author: str, limit: int = 10) -> List[BookSnapshot]:
        data = await self._get("/catalog/books", params={
            "author": author,
            "page": 1,
            "page_size": limit,
        })
        if not data:
            return []
        items = data.get("items", []) if isinstance(data, dict) else []
        return [self._to_snapshot(b) for b in items]