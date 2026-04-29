import httpx
import os
import uuid
from typing import Optional
from app.domain.providers import EnrichmentProvider
from app.domain.entities import EnrichmentResult

GOOGLE_BOOKS_URL = "https://www.googleapis.com/books/v1/volumes"
TIMEOUT = int(os.getenv("ENRICHMENT_TIMEOUT_SECONDS", "10"))


class GoogleBooksAdapter(EnrichmentProvider):
    async def enrich(self, book_reference: str, title: str, author: str, isbn: str = None) -> EnrichmentResult:
        try:
            query = f"isbn:{isbn}" if isbn else f"intitle:{title}+inauthor:{author}"
            async with httpx.AsyncClient(timeout=TIMEOUT) as client:
                r = await client.get(GOOGLE_BOOKS_URL, params={"q": query, "maxResults": 1})
                r.raise_for_status()
                data = r.json()
            items = data.get("items", [])
            if not items:
                raise Exception("No results")
            info = items[0].get("volumeInfo", {})
            image_links = info.get("imageLinks", {})
            return EnrichmentResult(
                id=uuid.uuid4(),
                request_id=uuid.uuid4(),
                normalized_title=info.get("title", title),
                normalized_author=", ".join(info.get("authors", [author])),
                normalized_publisher=info.get("publisher", ""),
                normalized_description=info.get("description", ""),
                cover_url=image_links.get("thumbnail", ""),
                metadata_json={"source": "google_books", "data": info},
            )
        except Exception:
            raise
