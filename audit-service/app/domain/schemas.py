import uuid
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from app.domain.entities import EventType


class AuditEventResponse(BaseModel):
    id: uuid.UUID
    event_type: EventType
    book_reference: str
    timestamp: datetime
    actor: str
    details: Optional[dict] = None

    class Config:
        from_attributes = True


class PricingHistoryItem(BaseModel):
    id: uuid.UUID
    book_reference: str
    suggested_price: Optional[float]
    explanation: Optional[str]
    condition_factor: Optional[float]
    source_used: Optional[str]
    timestamp: datetime

    class Config:
        from_attributes = True


class EnrichmentHistoryItem(BaseModel):
    id: uuid.UUID
    book_reference: str
    source_used: Optional[str]
    status: Optional[str]
    normalized_title: Optional[str]
    normalized_author: Optional[str]
    timestamp: datetime

    class Config:
        from_attributes = True


class BookSummaryResponse(BaseModel):
    book_reference: str
    pricing_history: List[PricingHistoryItem]
    enrichment_history: List[EnrichmentHistoryItem]
    total_pricing_decisions: int
    total_enrichments: int
