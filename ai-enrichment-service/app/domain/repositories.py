from abc import ABC, abstractmethod
from typing import Optional
import uuid
from app.domain.entities import EnrichmentRequest, EnrichmentResult


class EnrichmentRequestRepository(ABC):

    @abstractmethod
    def save(self, request: EnrichmentRequest) -> EnrichmentRequest:
        pass

    @abstractmethod
    def get_by_id(self, request_id: uuid.UUID) -> Optional[EnrichmentRequest]:
        pass

    @abstractmethod
    def update_status(self, request_id: uuid.UUID, status: str, source_used: str) -> EnrichmentRequest:
        pass

    @abstractmethod
    def get_by_book_reference(self, book_reference: str) -> list[EnrichmentRequest]:
        pass


class EnrichmentResultRepository(ABC):

    @abstractmethod
    def save(self, result: EnrichmentResult) -> EnrichmentResult:
        pass

    @abstractmethod
    def get_by_request_id(self, request_id: uuid.UUID) -> Optional[EnrichmentResult]:
        pass