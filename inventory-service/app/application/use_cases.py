import uuid
from datetime import datetime
from typing import Optional, List
from app.domain.entities import InventoryItem, ImportBatch, ImportError, BatchStatus, Condition
from app.domain.repositories import InventoryRepository, ImportBatchRepository, ImportErrorRepository
from app.domain.validators import build_validator_chain
from app.domain.error_hints import ERROR_HINTS
from app.domain.schemas import ImportBatchResponse, ImportErrorResponse, BatchSummaryResponse
from app.infrastructure.parsers.factory import FileParserFactory


class ProcessInventoryFile:

    def __init__(
        self,
        inventory_repo: InventoryRepository,
        batch_repo: ImportBatchRepository,
        error_repo: ImportErrorRepository,
    ):
        self.inventory_repo = inventory_repo
        self.batch_repo = batch_repo
        self.error_repo = error_repo

    def execute(self, file_bytes: bytes, file_name: str) -> ImportBatchResponse:
        extension = file_name.split(".")[-1]
        try:
            parser = FileParserFactory.get_parser(extension)
        except ValueError:
            raise ValueError("UNSUPPORTED_FORMAT")

        rows = parser.parse(file_bytes)
        total_rows = len(rows)

        batch = ImportBatch(
            id=uuid.uuid4(),
            file_name=file_name,
            upload_date=datetime.utcnow(),
            total_rows=total_rows,
            valid_rows=0,
            invalid_rows=0,
            status=BatchStatus.PROCESSING,
        )
        batch = self.batch_repo.save(batch)

        validator = build_validator_chain()
        valid_count = 0
        invalid_count = 0

        for index, row in enumerate(rows, start=1):
            row_str = {k: str(v) if v is not None else "" for k, v in row.items()}
            result = validator.validate(row_str)

            if result and not result.is_valid:
                invalid_count += 1
                error = ImportError(
                    id=uuid.uuid4(),
                    batch_id=batch.id,
                    row_number=index,
                    error_type=result.error_type,
                    message=result.message,
                )
                self.error_repo.save(error)
            else:
                valid_count += 1
                item = InventoryItem(
                    id=uuid.uuid4(),
                    external_code=row_str.get("external_code", ""),
                    book_reference=row_str.get("book_reference", ""),
                    quantity_available=int(row.get("quantity_available", 0)),
                    quantity_reserved=int(row.get("quantity_reserved", 0)),
                    condition=Condition(row_str.get("condition")),
                    defects=row_str.get("defects") or None,
                    observations=row_str.get("observations") or None,
                    import_batch_id=batch.id,
                )
                self.inventory_repo.save(item)

        batch.valid_rows = valid_count
        batch.invalid_rows = invalid_count
        batch.status = BatchStatus.COMPLETED
        batch = self.batch_repo.update(batch)

        success_percentage = (valid_count / total_rows * 100) if total_rows > 0 else 0

        return ImportBatchResponse(
            id=batch.id,
            file_name=batch.file_name,
            upload_date=batch.upload_date,
            total_rows=batch.total_rows,
            valid_rows=batch.valid_rows,
            invalid_rows=batch.invalid_rows,
            status=batch.status,
            success_percentage=round(success_percentage, 2),
        )


class GetBatches:

    def __init__(self, batch_repo: ImportBatchRepository):
        self.batch_repo = batch_repo

    def execute(self, page: int, page_size: int) -> tuple[List[ImportBatchResponse], int]:
        batches, total = self.batch_repo.get_all(page, page_size)
        items = [
            ImportBatchResponse(
                id=b.id,
                file_name=b.file_name,
                upload_date=b.upload_date,
                total_rows=b.total_rows,
                valid_rows=b.valid_rows,
                invalid_rows=b.invalid_rows,
                status=b.status,
                success_percentage=round(b.valid_rows / b.total_rows * 100, 2) if b.total_rows > 0 else 0,
            )
            for b in batches
        ]
        return items, total


class GetBatchById:

    def __init__(self, batch_repo: ImportBatchRepository):
        self.batch_repo = batch_repo

    def execute(self, batch_id: uuid.UUID) -> ImportBatchResponse:
        batch = self.batch_repo.get_by_id(batch_id)
        if not batch:
            raise ValueError("BATCH_NOT_FOUND")
        return ImportBatchResponse(
            id=batch.id,
            file_name=batch.file_name,
            upload_date=batch.upload_date,
            total_rows=batch.total_rows,
            valid_rows=batch.valid_rows,
            invalid_rows=batch.invalid_rows,
            status=batch.status,
            success_percentage=round(batch.valid_rows / batch.total_rows * 100, 2) if batch.total_rows > 0 else 0,
        )


class GetBatchErrors:

    def __init__(self, error_repo: ImportErrorRepository):
        self.error_repo = error_repo

    def execute(self, batch_id: uuid.UUID, error_type: Optional[str]) -> List[ImportErrorResponse]:
        errors = self.error_repo.get_by_batch(batch_id, error_type)
        return [
            ImportErrorResponse(
                id=e.id,
                batch_id=e.batch_id,
                row_number=e.row_number,
                error_type=e.error_type,
                message=e.message,
                fix_hint=ERROR_HINTS.get(e.error_type),
            )
            for e in errors
        ]


class GetBatchSummary:

    def __init__(self, batch_repo: ImportBatchRepository, error_repo: ImportErrorRepository):
        self.batch_repo = batch_repo
        self.error_repo = error_repo

    def execute(self, batch_id: uuid.UUID) -> BatchSummaryResponse:
        batch = self.batch_repo.get_by_id(batch_id)
        if not batch:
            raise ValueError("BATCH_NOT_FOUND")

        errors = self.error_repo.get_by_batch(batch_id, None)
        error_counts: dict = {}
        for error in errors:
            error_counts[error.error_type] = error_counts.get(error.error_type, 0) + 1

        most_frequent = [
            {"error_type": k, "count": v}
            for k, v in sorted(error_counts.items(), key=lambda x: x[1], reverse=True)
        ]

        return BatchSummaryResponse(
            batch_id=batch.id,
            total_rows=batch.total_rows,
            valid_rows=batch.valid_rows,
            invalid_rows=batch.invalid_rows,
            success_percentage=round(batch.valid_rows / batch.total_rows * 100, 2) if batch.total_rows > 0 else 0,
            most_frequent_errors=most_frequent,
        )
