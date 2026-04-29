from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class EnrichmentResultInput(BaseModel):
    enrichment_result_id: str
    title: str
    author: str
    isbn: Optional[str] = None
    issn: Optional[str] = None


class NormalizedRecordResponse(BaseModel):
    id: str
    enrichment_result_id: str
    normalized_title: str
    normalized_author: str
    normalized_isbn: Optional[str] = None
    isbn_valid: bool
    issn_valid: bool
    is_duplicate: bool
    duplicate_of_id: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class BatchInput(BaseModel):
    records: List[EnrichmentResultInput]


class BatchResponse(BaseModel):
    processed: int
    results: List[NormalizedRecordResponse]
