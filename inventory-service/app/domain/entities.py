import uuid
from datetime import datetime
from typing import Optional
from enum import Enum


class Condition(str, Enum):
    NEW = "new"
    GOOD = "good"
    WORN = "worn"
    DAMAGED = "damaged"


class BatchStatus(str, Enum):
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class InventoryItem:
    def __init__(
        self,
        id: uuid.UUID,
        external_code: str,
        book_reference: str,
        quantity_available: int,
        quantity_reserved: int,
        condition: Condition,
        defects: Optional[str],
        observations: Optional[str],
        import_batch_id: uuid.UUID,
    ):
        self.id = id
        self.external_code = external_code
        self.book_reference = book_reference
        self.quantity_available = quantity_available
        self.quantity_reserved = quantity_reserved
        self.condition = condition
        self.defects = defects
        self.observations = observations
        self.import_batch_id = import_batch_id


class ImportBatch:
    def __init__(
        self,
        id: uuid.UUID,
        file_name: str,
        upload_date: datetime,
        total_rows: int,
        valid_rows: int,
        invalid_rows: int,
        status: BatchStatus,
    ):
        self.id = id
        self.file_name = file_name
        self.upload_date = upload_date
        self.total_rows = total_rows
        self.valid_rows = valid_rows
        self.invalid_rows = invalid_rows
        self.status = status


class ImportError:
    def __init__(
        self,
        id: uuid.UUID,
        batch_id: uuid.UUID,
        row_number: int,
        error_type: str,
        message: str,
    ):
        self.id = id
        self.batch_id = batch_id
        self.row_number = row_number
        self.error_type = error_type
        self.message = message
