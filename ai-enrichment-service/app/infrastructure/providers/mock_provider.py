import uuid
import asyncio
import os
from dotenv import load_dotenv
from app.domain.providers import EnrichmentProvider
from app.domain.entities import EnrichmentResult

load_dotenv()

MOCK_LATENCY_MS = int(os.getenv("MOCK_LATENCY_MS", 500))


class MockEnrichmentProvider(EnrichmentProvider):

    async def enrich(self, book_reference: str, title: str, author: str, isbn: str) -> EnrichmentResult:
        await asyncio.sleep(MOCK_LATENCY_MS / 1000)
        return EnrichmentResult(
            id=uuid.uuid4(),
            request_id=uuid.uuid4(),
            normalized_title=f"[MOCK] {title or 'Unknown Title'}",
            normalized_author=f"[MOCK] {author or 'Unknown Author'}",
            normalized_publisher="[MOCK] Editorial Example",
            normalized_description="[MOCK] This is a mock description generated for testing purposes.",
            cover_url="https://via.placeholder.com/150",
            metadata_json={"source": "mock", "book_reference": book_reference, "isbn": isbn},
        )
