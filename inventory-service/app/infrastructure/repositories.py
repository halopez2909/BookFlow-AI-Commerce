import uuid
from typing import Optional, List
from sqlalchemy.orm import Session
from app.domain.entities import InventoryItem, ImportBatch, ImportError, BatchStatus, Condition
from app.domain.repositories import InventoryRepository, ImportBatchRepository, ImportErrorRepository
from app.infrastructure.models import InventoryItemModel, ImportBatchModel, ImportErrorModel


class InventoryRepositoryPostgres(InventoryRepository):

    def __init__(self, db: Session):
        self.db = db

    def save(self, item: InventoryItem) -> InventoryItem:
        model = InventoryItemModel(
            id=item.id,
            external_code=item.external_code,
            book_reference=item.book_reference,
            quantity_available=item.quantity_available,
            quantity_reserved=item.quantity_reserved,
            condition=item.condition.value,
            defects=item.defects,
            observations=item.observations,
            import_batch_id=item.import_batch_id,
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return self._to_entity(model)

    def get_by_id(self, item_id: uuid.UUID) -> Optional[InventoryItem]:
        model = self.db.query(InventoryItemModel).filter(InventoryItemModel.id == item_id).first()
        if not model:
            return None
        return self._to_entity(model)

    def get_by_batch(self, batch_id: uuid.UUID) -> List[InventoryItem]:
        models = self.db.query(InventoryItemModel).filter(InventoryItemModel.import_batch_id == batch_id).all()
        return [self._to_entity(m) for m in models]

    def _to_entity(self, model: InventoryItemModel) -> InventoryItem:
        return InventoryItem(
            id=model.id,
            external_code=model.external_code,
            book_reference=model.book_reference,
            quantity_available=model.quantity_available,
            quantity_reserved=model.quantity_reserved,
            condition=Condition(model.condition),
            defects=model.defects,
            observations=model.observations,
            import_batch_id=model.import_batch_id,
        )


class ImportBatchRepositoryPostgres(ImportBatchRepository):

    def __init__(self, db: Session):
        self.db = db

    def save(self, batch: ImportBatch) -> ImportBatch:
        model = ImportBatchModel(
            id=batch.id,
            file_name=batch.file_name,
            upload_date=batch.upload_date,
            total_rows=batch.total_rows,
            valid_rows=batch.valid_rows,
            invalid_rows=batch.invalid_rows,
            status=batch.status.value,
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return self._to_entity(model)

    def get_by_id(self, batch_id: uuid.UUID) -> Optional[ImportBatch]:
        model = self.db.query(ImportBatchModel).filter(ImportBatchModel.id == batch_id).first()
        if not model:
            return None
        return self._to_entity(model)

    def get_all(self, page: int, page_size: int) -> tuple[List[ImportBatch], int]:
        query = self.db.query(ImportBatchModel)
        total = query.count()
        models = query.offset((page - 1) * page_size).limit(page_size).all()
        return [self._to_entity(m) for m in models], total

    def update(self, batch: ImportBatch) -> ImportBatch:
        model = self.db.query(ImportBatchModel).filter(ImportBatchModel.id == batch.id).first()
        model.valid_rows = batch.valid_rows
        model.invalid_rows = batch.invalid_rows
        model.status = batch.status.value
        self.db.commit()
        self.db.refresh(model)
        return self._to_entity(model)

    def _to_entity(self, model: ImportBatchModel) -> ImportBatch:
        return ImportBatch(
            id=model.id,
            file_name=model.file_name,
            upload_date=model.upload_date,
            total_rows=model.total_rows,
            valid_rows=model.valid_rows,
            invalid_rows=model.invalid_rows,
            status=BatchStatus(model.status),
        )


class ImportErrorRepositoryPostgres(ImportErrorRepository):

    def __init__(self, db: Session):
        self.db = db

    def save(self, error: ImportError) -> ImportError:
        model = ImportErrorModel(
            id=error.id,
            batch_id=error.batch_id,
            row_number=error.row_number,
            error_type=error.error_type,
            message=error.message,
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return self._to_entity(model)

    def get_by_batch(self, batch_id: uuid.UUID, error_type: Optional[str]) -> List[ImportError]:
        query = self.db.query(ImportErrorModel).filter(ImportErrorModel.batch_id == batch_id)
        if error_type:
            query = query.filter(ImportErrorModel.error_type == error_type)
        models = query.all()
        return [self._to_entity(m) for m in models]

    def _to_entity(self, model: ImportErrorModel) -> ImportError:
        return ImportError(
            id=model.id,
            batch_id=model.batch_id,
            row_number=model.row_number,
            error_type=model.error_type,
            message=model.message,
        )
