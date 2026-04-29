from typing import List, Optional
from sqlalchemy.orm import Session
from app.domain.entities import NormalizedRecord
from app.domain.repositories import NormalizedRecordRepository
from app.infrastructure.models import NormalizedRecordModel
from datetime import datetime


class NormalizedRecordRepositoryPostgres(NormalizedRecordRepository):
    def __init__(self, db: Session):
        self.db = db

    def save(self, record: NormalizedRecord) -> NormalizedRecord:
        model = NormalizedRecordModel(
            id=record.id,
            enrichment_result_id=record.enrichment_result_id,
            normalized_title=record.normalized_title,
            normalized_author=record.normalized_author,
            normalized_isbn=record.normalized_isbn,
            isbn_valid=record.isbn_valid,
            issn_valid=record.issn_valid,
            is_duplicate=record.is_duplicate,
            duplicate_of_id=record.duplicate_of_id,
            created_at=record.created_at,
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return record

    def find_all(self) -> List[NormalizedRecord]:
        models = self.db.query(NormalizedRecordModel).all()
        return [self._to_entity(m) for m in models]

    def find_by_id(self, record_id: str) -> Optional[NormalizedRecord]:
        model = self.db.query(NormalizedRecordModel).filter(
            NormalizedRecordModel.id == record_id
        ).first()
        return self._to_entity(model) if model else None

    def _to_entity(self, model: NormalizedRecordModel) -> NormalizedRecord:
        return NormalizedRecord(
            id=model.id,
            enrichment_result_id=model.enrichment_result_id,
            normalized_title=model.normalized_title,
            normalized_author=model.normalized_author,
            normalized_isbn=model.normalized_isbn,
            isbn_valid=model.isbn_valid,
            issn_valid=model.issn_valid,
            is_duplicate=model.is_duplicate,
            duplicate_of_id=model.duplicate_of_id,
            created_at=model.created_at,
        )
