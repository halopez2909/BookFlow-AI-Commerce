from pydantic import BaseModel
from typing import Optional, Any
import uuid
from datetime import datetime
from app.domain.entities import EnrichmentStatus


class EnrichBookRequest(BaseModel):
    book_reference: str
    title: Optional[str] = None
    author: Optional[str] = None
    isbn: Optional[str] = None


class EnrichmentResultResponse(BaseModel):
    id: uuid.UUID
    request_id: uuid.UUID
    normalized_title: Optional[str] = None
    normalized_author: Optional[str] = None
    normalized_publisher: Optional[str] = None
    normalized_description: Optional[str] = None
    cover_url: Optional[str] = None
    metadata_json: Optional[Any] = None

    model_config = {"from_attributes": True}


class EnrichmentRequestResponse(BaseModel):
    id: uuid.UUID
    book_reference: str
    status: EnrichmentStatus
    requested_at: datetime
    source_used: Optional[str] = None

    model_config = {"from_attributes": True}
