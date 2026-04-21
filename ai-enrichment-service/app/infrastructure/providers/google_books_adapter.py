import os
import uuid
import httpx
from dotenv import load_dotenv

from app.domain.providers import EnrichmentProvider
from app.domain.entities import EnrichmentResult

load_dotenv()


class GoogleBooksAdapter(EnrichmentProvider):
    def __init__(self):
        self.base_url = "https://www.googleapis.com/books/v1/volumes"
        self.timeout = float(os.getenv("ENRICHMENT_TIMEOUT_SECONDS", 5))
        self.api_key = os.getenv("GOOGLE_BOOKS_API_KEY", "")

    async def enrich(self, book_reference: str, title: str, author: str, isbn: str) -> EnrichmentResult:
        query = self._build_query(title=title, author=author, isbn=isbn)

        params = {"q": query}
        if self.api_key:
            params["key"] = self.api_key

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()

        items = data.get("items", [])
        if not items:
            raise ValueError("GOOGLE_BOOKS_NO_RESULTS")

        volume_info = items[0].get("volumeInfo", {})
        image_links = volume_info.get("imageLinks", {})

        return EnrichmentResult(
            id=uuid.uuid4(),
            request_id=uuid.uuid4(),
            normalized_title=volume_info.get("title") or title or None,
            normalized_author=", ".join(volume_info.get("authors", [])) if volume_info.get("authors") else (author or None),
            normalized_publisher=volume_info.get("publisher"),
            normalized_description=volume_info.get("description"),
            cover_url=image_links.get("thumbnail") or image_links.get("smallThumbnail"),
            metadata_json={
                "source": "google_books",
                "book_reference": book_reference,
                "isbn": isbn,
                "raw_total_items": data.get("totalItems", 0),
            },
            source_used="google_books",
        )

    def _build_query(self, title: str, author: str, isbn: str) -> str:
        if isbn:
            return f"isbn:{isbn}"

        query_parts = []
        if title:
            query_parts.append(f'intitle:"{title}"')
        if author:
            query_parts.append(f'inauthor:"{author}"')

        return " ".join(query_parts) if query_parts else "books"