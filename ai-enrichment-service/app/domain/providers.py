from abc import ABC, abstractmethod
from app.domain.entities import EnrichmentResult
import uuid


class EnrichmentProvider(ABC):

    @abstractmethod
    async def enrich(self, book_reference: str, title: str, author: str, isbn: str) -> EnrichmentResult:
        pass
