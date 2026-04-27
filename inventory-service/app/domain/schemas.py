from pydantic import BaseModel, field_validator
from typing import Optional, List
import uuid
from datetime import datetime
from app.domain.entities import Condition, BatchStatus


class InventoryRowSchema(BaseModel):
    external_code: str
    book_reference: str
    quantity_available: int
    quantity_reserved: int = 0
    condition: Condition
    defects: Optional[str] = None
    observations: Optional[str] = None

    @field_validator("defects")
    @classmethod
    def defects_required_for_worn_or_damaged(cls, v, info):
        condition = info.data.get("condition")
        if condition in (Condition.WORN, Condition.DAMAGED) and not v:
            raise ValueError("Defects are required for worn or damaged items")
        return v


class ImportBatchResponse(BaseModel):
    id: uuid.UUID
    file_name: str
    upload_date: datetime
    total_rows: int
    valid_rows: int
    invalid_rows: int
    status: BatchStatus
    success_percentage: Optional[float] = None

    model_config = {"from_attributes": True}


class ImportErrorResponse(BaseModel):
    id: uuid.UUID
    batch_id: uuid.UUID
    row_number: int
    error_type: str
    message: str
    fix_hint: Optional[str] = None

    model_config = {"from_attributes": True}


class BatchSummaryResponse(BaseModel):
    batch_id: uuid.UUID
    total_rows: int
    valid_rows: int
    invalid_rows: int
    success_percentage: float
    most_frequent_errors: List[dict]
