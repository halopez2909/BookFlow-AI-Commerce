import uuid
from typing import Optional
from sqlalchemy.orm import Session
from app.domain.entities import EnrichmentRequest, EnrichmentResult, EnrichmentStatus
from app.domain.repositories import EnrichmentRequestRepository, EnrichmentResultRepository
from app.infrastructure.models import EnrichmentRequestModel, EnrichmentResultModel


class EnrichmentRequestRepositoryPostgres(EnrichmentRequestRepository):

    def __init__(self, db: Session):
        self.db = db

    def save(self, request: EnrichmentRequest) -> EnrichmentRequest:
        model = EnrichmentRequestModel(
            id=request.id,
            book_reference=request.book_reference,
            title=request.title,
            author=request.author,
            isbn=request.isbn,
            status=request.status.value,
            requested_at=request.requested_at,
            source_used=request.source_used,
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return self._to_entity(model)

    def get_by_id(self, request_id: uuid.UUID) -> Optional[EnrichmentRequest]:
        model = self.db.query(EnrichmentRequestModel).filter(EnrichmentRequestModel.id == request_id).first()
        if not model:
            return None
        return self._to_entity(model)

    def get_by_book_reference(self, book_reference: str) -> list[EnrichmentRequest]:
        models = (
            self.db.query(EnrichmentRequestModel)
            .filter(EnrichmentRequestModel.book_reference == book_reference)
            .order_by(EnrichmentRequestModel.requested_at.desc())
            .all()
        )
        return [self._to_entity(model) for model in models]

    def update_status(self, request_id: uuid.UUID, status: str, source_used: str) -> EnrichmentRequest:
        model = self.db.query(EnrichmentRequestModel).filter(EnrichmentRequestModel.id == request_id).first()
        model.status = status
        model.source_used = source_used
        self.db.commit()
        self.db.refresh(model)
        return self._to_entity(model)

    def _to_entity(self, model: EnrichmentRequestModel) -> EnrichmentRequest:
        return EnrichmentRequest(
            id=model.id,
            book_reference=model.book_reference,
            title=model.title,
            author=model.author,
            isbn=model.isbn,
            status=EnrichmentStatus(model.status),
            requested_at=model.requested_at,
            source_used=model.source_used,
        )


class EnrichmentResultRepositoryPostgres(EnrichmentResultRepository):

    def __init__(self, db: Session):
        self.db = db

    def save(self, result: EnrichmentResult) -> EnrichmentResult:
        model = EnrichmentResultModel(
            id=result.id,
            request_id=result.request_id,
            normalized_title=result.normalized_title,
            normalized_author=result.normalized_author,
            normalized_publisher=result.normalized_publisher,
            normalized_description=result.normalized_description,
            cover_url=result.cover_url,
            metadata_json=result.metadata_json,
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return self._to_entity(model)

    def get_by_request_id(self, request_id: uuid.UUID) -> Optional[EnrichmentResult]:
        model = self.db.query(EnrichmentResultModel).filter(EnrichmentResultModel.request_id == request_id).first()
        if not model:
            return None
        return self._to_entity(model)

    def _to_entity(self, model: EnrichmentResultModel) -> EnrichmentResult:
        return EnrichmentResult(
            id=model.id,
            request_id=model.request_id,
            normalized_title=model.normalized_title,
            normalized_author=model.normalized_author,
            normalized_publisher=model.normalized_publisher,
            normalized_description=model.normalized_description,
            cover_url=model.cover_url,
            metadata_json=model.metadata_json,
        )