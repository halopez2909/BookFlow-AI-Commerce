import httpx
import os
import uuid
from app.domain.providers import EnrichmentProvider
from app.domain.entities import EnrichmentResult

TIMEOUT = int(os.getenv("ENRICHMENT_TIMEOUT_SECONDS", "10"))
OPEN_LIBRARY_URL = "https://openlibrary.org/search.json"


class OpenLibraryAdapter(EnrichmentProvider):
    async def enrich(self, book_reference: str, title: str, author: str, isbn: str = None) -> EnrichmentResult:
        try:
            params = {"isbn": isbn} if isbn else {"title": title, "author": author}
            params["limit"] = 1
            async with httpx.AsyncClient(timeout=TIMEOUT) as client:
                r = await client.get(OPEN_LIBRARY_URL, params=params)
                r.raise_for_status()
                data = r.json()
            docs = data.get("docs", [])
            if not docs:
                raise Exception("No results")
            doc = docs[0]
            cover_id = doc.get("cover_i")
            cover_url = f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg" if cover_id else ""
            return EnrichmentResult(
                id=uuid.uuid4(),
                request_id=uuid.uuid4(),
                normalized_title=doc.get("title", title),
                normalized_author=", ".join(doc.get("author_name", [author])),
                normalized_publisher=", ".join(doc.get("publisher", [])[:1]),
                normalized_description="",
                cover_url=cover_url,
                metadata_json={"source": "open_library", "data": doc},
            )
        except Exception:
            raise
