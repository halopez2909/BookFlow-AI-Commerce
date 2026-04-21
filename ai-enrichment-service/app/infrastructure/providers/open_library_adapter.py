import os
import uuid
import httpx
from dotenv import load_dotenv

from app.domain.providers import EnrichmentProvider
from app.domain.entities import EnrichmentResult

load_dotenv()


class OpenLibraryAdapter(EnrichmentProvider):
    def __init__(self):
        self.base_url = "https://openlibrary.org/search.json"
        self.timeout = float(os.getenv("ENRICHMENT_TIMEOUT_SECONDS", 5))

    async def enrich(self, book_reference: str, title: str, author: str, isbn: str) -> EnrichmentResult:
        params = self._build_params(title=title, author=author, isbn=isbn)

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()

        docs = data.get("docs", [])
        if not docs:
            raise ValueError("OPEN_LIBRARY_NO_RESULTS")

        book = docs[0]

        cover_url = None
        cover_i = book.get("cover_i")
        if cover_i:
            cover_url = f"https://covers.openlibrary.org/b/id/{cover_i}-L.jpg"

        author_name = None
        if book.get("author_name"):
            author_name = ", ".join(book.get("author_name"))

        publisher = None
        if book.get("publisher"):
            publisher = book["publisher"][0]

        first_sentence = None
        if book.get("first_sentence"):
            if isinstance(book["first_sentence"], list):
                first_sentence = book["first_sentence"][0]
            else:
                first_sentence = str(book["first_sentence"])

        return EnrichmentResult(
            id=uuid.uuid4(),
            request_id=uuid.uuid4(),
            normalized_title=book.get("title") or title or None,
            normalized_author=author_name or author or None,
            normalized_publisher=publisher,
            normalized_description=first_sentence or "Información obtenida desde Open Library.",
            cover_url=cover_url,
            metadata_json={
                "source": "open_library",
                "book_reference": book_reference,
                "isbn": isbn,
                "num_found": data.get("numFound", 0),
            },
            source_used="open_library",
        )

    def _build_params(self, title: str, author: str, isbn: str) -> dict:
        if isbn:
            return {"isbn": isbn}

        params = {}
        if title:
            params["title"] = title
        if author:
            params["author"] = author

        return params if params else {"q": "books"}