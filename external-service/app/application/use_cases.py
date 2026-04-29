from typing import Optional, List
from datetime import datetime
from app.domain.entities import ExternalApiResult, ApiHealthStatus
from app.domain.schemas import BookLookupRequest
from app.infrastructure.google_books_client import GoogleBooksClient
from app.infrastructure.open_library_client import OpenLibraryClient
from app.infrastructure.crossref_client import CrossrefClient


class LookupBookExternal:
    def __init__(self):
        self.google = GoogleBooksClient()
        self.open_library = OpenLibraryClient()
        self.crossref = CrossrefClient()

    async def execute(self, request: BookLookupRequest) -> ExternalApiResult:
        # Try Google Books first
        result = await self.google.lookup(request.isbn, request.title, request.author)
        if result.success:
            return result

        # Fallback to Open Library
        result = await self.open_library.lookup(request.isbn, request.title, request.author)
        if result.success:
            return result

        # Fallback to Crossref if ISSN provided
        if request.issn:
            result = await self.crossref.lookup_by_issn(request.issn)
            if result.success:
                return result

        # Final fallback
        return ExternalApiResult.fail(
            source="all_sources",
            error="No external source returned results",
            latency_ms=0,
        )


class CheckExternalHealth:
    def __init__(self):
        self.google = GoogleBooksClient()
        self.open_library = OpenLibraryClient()
        self.crossref = CrossrefClient()

    async def execute(self) -> List[ApiHealthStatus]:
        results = []
        now = datetime.utcnow()

        gb = await self.google.health_check()
        results.append(ApiHealthStatus(
            name="google_books", status=gb["status"],
            latency_ms=gb["latency_ms"], last_checked=now,
            error=gb.get("error"),
        ))

        ol = await self.open_library.health_check()
        results.append(ApiHealthStatus(
            name="open_library", status=ol["status"],
            latency_ms=ol["latency_ms"], last_checked=now,
            error=ol.get("error"),
        ))

        cr = await self.crossref.health_check()
        results.append(ApiHealthStatus(
            name="crossref", status=cr["status"],
            latency_ms=cr["latency_ms"], last_checked=now,
            error=cr.get("error"),
        ))

        return results
