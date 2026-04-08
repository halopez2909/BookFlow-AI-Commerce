from app.domain.providers import EnrichmentProvider
from app.domain.entities import EnrichmentResult


class GoogleBooksAdapter(EnrichmentProvider):

    async def enrich(self, book_reference: str, title: str, author: str, isbn: str) -> EnrichmentResult:
        raise NotImplementedError("GoogleBooksAdapter will be implemented in Sprint 2")
