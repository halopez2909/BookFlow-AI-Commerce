# Google Books Adapter
google_books = """import httpx
import os
from typing import Optional
from app.domain.providers import EnrichmentProvider
from app.domain.entities import EnrichmentResult, EnrichmentStatus
import uuid
from datetime import datetime


GOOGLE_BOOKS_URL = "https://www.googleapis.com/books/v1/volumes"
TIMEOUT = int(os.getenv("ENRICHMENT_TIMEOUT_SECONDS", "10"))


class GoogleBooksAdapter(EnrichmentProvider):
    async def enrich(self, book_reference: str, title: str, author: str, isbn: Optional[str] = None) -> EnrichmentResult:
        try:
            query = f"isbn:{isbn}" if isbn else f"intitle:{title}+inauthor:{author}"
            async with httpx.AsyncClient(timeout=TIMEOUT) as client:
                r = await client.get(GOOGLE_BOOKS_URL, params={"q": query, "maxResults": 1})
                r.raise_for_status()
                data = r.json()

            items = data.get("items", [])
            if not items:
                return await self._fallback(book_reference, title, author, isbn)

            info = items[0].get("volumeInfo", {})
            image_links = info.get("imageLinks", {})

            return EnrichmentResult(
                id=str(uuid.uuid4()),
                book_reference=book_reference,
                status=EnrichmentStatus.COMPLETED,
                normalized_title=info.get("title", title),
                normalized_author=", ".join(info.get("authors", [author])),
                normalized_publisher=info.get("publisher", ""),
                normalized_description=info.get("description", ""),
                cover_url=image_links.get("thumbnail", ""),
                source_used="google_books",
                metadata_json=str(info),
                created_at=datetime.utcnow(),
            )
        except Exception:
            return await self._fallback(book_reference, title, author, isbn)

    async def _fallback(self, book_reference, title, author, isbn):
        return EnrichmentResult(
            id=str(uuid.uuid4()),
            book_reference=book_reference,
            status=EnrichmentStatus.COMPLETED,
            normalized_title=title,
            normalized_author=author,
            normalized_publisher="",
            normalized_description="",
            cover_url="",
            source_used="fallback_interno",
            metadata_json="{}",
            created_at=datetime.utcnow(),
        )
"""

# Open Library Adapter
open_library = """import httpx
import os
from typing import Optional
from app.domain.providers import EnrichmentProvider
from app.domain.entities import EnrichmentResult, EnrichmentStatus
import uuid
from datetime import datetime

TIMEOUT = int(os.getenv("ENRICHMENT_TIMEOUT_SECONDS", "10"))
OPEN_LIBRARY_URL = "https://openlibrary.org/search.json"


class OpenLibraryAdapter(EnrichmentProvider):
    async def enrich(self, book_reference: str, title: str, author: str, isbn: Optional[str] = None) -> EnrichmentResult:
        try:
            params = {"isbn": isbn} if isbn else {"title": title, "author": author}
            params["limit"] = 1
            async with httpx.AsyncClient(timeout=TIMEOUT) as client:
                r = await client.get(OPEN_LIBRARY_URL, params=params)
                r.raise_for_status()
                data = r.json()

            docs = data.get("docs", [])
            if not docs:
                return self._fallback(book_reference, title, author)

            doc = docs[0]
            cover_id = doc.get("cover_i")
            cover_url = f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg" if cover_id else ""

            return EnrichmentResult(
                id=str(uuid.uuid4()),
                book_reference=book_reference,
                status=EnrichmentStatus.COMPLETED,
                normalized_title=doc.get("title", title),
                normalized_author=", ".join(doc.get("author_name", [author])),
                normalized_publisher=", ".join(doc.get("publisher", [])[:1]),
                normalized_description="",
                cover_url=cover_url,
                source_used="open_library",
                metadata_json=str(doc),
                created_at=datetime.utcnow(),
            )
        except Exception:
            return self._fallback(book_reference, title, author)

    def _fallback(self, book_reference, title, author):
        return EnrichmentResult(
            id=str(uuid.uuid4()),
            book_reference=book_reference,
            status=EnrichmentStatus.COMPLETED,
            normalized_title=title,
            normalized_author=author,
            normalized_publisher="",
            normalized_description="",
            cover_url="",
            source_used="fallback_interno",
            metadata_json="{}",
            created_at=datetime.utcnow(),
        )
"""

# Fallback Provider
fallback = """from typing import Optional
from app.domain.providers import EnrichmentProvider
from app.domain.entities import EnrichmentResult, EnrichmentStatus
import uuid
from datetime import datetime


class FallbackProvider(EnrichmentProvider):
    async def enrich(self, book_reference: str, title: str, author: str, isbn: Optional[str] = None) -> EnrichmentResult:
        return EnrichmentResult(
            id=str(uuid.uuid4()),
            book_reference=book_reference,
            status=EnrichmentStatus.COMPLETED,
            normalized_title=title,
            normalized_author=author,
            normalized_publisher="",
            normalized_description="",
            cover_url="",
            source_used="fallback_interno",
            metadata_json="{}",
            created_at=datetime.utcnow(),
        )
"""

# Updated Factory with Chain of Responsibility
factory = """import os
from app.domain.providers import EnrichmentProvider
from app.infrastructure.providers.mock_provider import MockEnrichmentProvider
from app.infrastructure.providers.google_books_adapter import GoogleBooksAdapter
from app.infrastructure.providers.open_library_adapter import OpenLibraryAdapter
from app.infrastructure.providers.fallback_provider import FallbackProvider
from dotenv import load_dotenv

load_dotenv()


class ChainedEnrichmentProvider(EnrichmentProvider):
    def __init__(self, providers):
        self.providers = providers

    async def enrich(self, book_reference, title, author, isbn=None):
        for provider in self.providers:
            try:
                result = await provider.enrich(book_reference, title, author, isbn)
                if result and result.source_used != "fallback_interno":
                    return result
            except Exception:
                continue
        return await FallbackProvider().enrich(book_reference, title, author, isbn)


class EnrichmentProviderFactory:
    @staticmethod
    def get_provider() -> EnrichmentProvider:
        provider = os.getenv("ENRICHMENT_PROVIDER", "mock")
        if provider == "mock":
            return MockEnrichmentProvider()
        elif provider == "google_books":
            return ChainedEnrichmentProvider([
                GoogleBooksAdapter(),
                OpenLibraryAdapter(),
                FallbackProvider(),
            ])
        return MockEnrichmentProvider()
"""

import os

files = {
    'ai-enrichment-service/app/infrastructure/providers/google_books_adapter.py': google_books,
    'ai-enrichment-service/app/infrastructure/providers/open_library_adapter.py': open_library,
    'ai-enrichment-service/app/infrastructure/providers/fallback_provider.py': fallback,
    'ai-enrichment-service/app/infrastructure/providers/factory.py': factory,
}

for path, content in files.items():
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Updated: {path}')

print('Enrichment service updated!')
