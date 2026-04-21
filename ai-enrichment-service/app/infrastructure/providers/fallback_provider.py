import uuid

from app.domain.providers import EnrichmentProvider
from app.domain.entities import EnrichmentResult


class FallbackProvider(EnrichmentProvider):
    async def enrich(self, book_reference: str, title: str, author: str, isbn: str) -> EnrichmentResult:
        return EnrichmentResult(
            id=uuid.uuid4(),
            request_id=uuid.uuid4(),
            normalized_title=title or None,
            normalized_author=author or None,
            normalized_publisher=None,
            normalized_description="No se encontró información externa. Se conservaron los datos originales.",
            cover_url=None,
            metadata_json={
                "source": "fallback_interno",
                "book_reference": book_reference,
                "isbn": isbn,
            },
            source_used="fallback_interno",
        )