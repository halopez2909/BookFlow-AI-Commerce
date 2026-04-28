import uuid
from datetime import datetime
from typing import Optional
from enum import Enum


class EventType(str, Enum):
    PRICING_DECISION = "pricing_decision"
    ENRICHMENT_COMPLETED = "enrichment_completed"
    NORMALIZATION_APPLIED = "normalization_applied"


class AuditEvent:
    def __init__(
        self,
        id: uuid.UUID,
        event_type: EventType,
        book_reference: str,
        timestamp: datetime,
        actor: str,
        details: Optional[dict] = None,
    ):
        self.id = id
        self.event_type = event_type
        self.book_reference = book_reference
        self.timestamp = timestamp
        self.actor = actor
        self.details = details or {}
