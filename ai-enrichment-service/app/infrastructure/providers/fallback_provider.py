import uuid
from app.domain.providers import EnrichmentProvider
from app.domain.entities import EnrichmentResult


class FallbackProvider(EnrichmentProvider):
    async def enrich(self, book_reference: str, title: str, author: str, isbn: str = None) -> EnrichmentResult:
        return EnrichmentResult(
            id=uuid.uuid4(),
            request_id=uuid.uuid4(),
            normalized_title=title,
            normalized_author=author,
            normalized_publisher="",
            normalized_description="",
            cover_url="",
            metadata_json={"source": "fallback_interno"},
        )
