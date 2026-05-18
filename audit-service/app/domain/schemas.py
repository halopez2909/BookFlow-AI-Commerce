import uuid
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from app.domain.entities import EventType


# ──────────────────────────────────────────
# Schemas existentes del Sprint 2
# ──────────────────────────────────────────

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


# ──────────────────────────────────────────
# Schemas nuevos del Sprint 3
# ──────────────────────────────────────────

class OrderItemAudit(BaseModel):
    book_id: str
    quantity: int
    unit_price: float

    class Config:
        from_attributes = True


class OrderHistoryItem(BaseModel):
    id: uuid.UUID
    customer_id: str
    status: str
    total_amount: Optional[float]
    created_at: datetime
    updated_at: Optional[datetime]
    items: List[OrderItemAudit] = []

    class Config:
        from_attributes = True


class CartItemAudit(BaseModel):
    book_id: str
    quantity: int
    unit_price: Optional[float]

    class Config:
        from_attributes = True


class CartHistoryItem(BaseModel):
    id: uuid.UUID
    customer_id: str
    status: str
    created_at: datetime
    updated_at: Optional[datetime]
    items: List[CartItemAudit] = []

    class Config:
        from_attributes = True


class AssistantInteractionItem(BaseModel):
    id: uuid.UUID
    session_id: str
    user_question: str
    interpreted_intent: Optional[str]
    answer_text: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


# Para GET /audit/global/events
class GlobalEventItem(BaseModel):
    id: uuid.UUID
    event_type: EventType
    book_reference: str
    timestamp: datetime
    actor: str
    details: Optional[dict] = None

    class Config:
        from_attributes = True


# Para GET /audit/global/summary
class GlobalSummaryResponse(BaseModel):
    period_days: int
    total_orders: int
    total_carts: int
    cart_to_order_rate: float           # % carritos que se convirtieron en pedido
    top_books: List[str]                # book_ids más consultados
    top_assistant_intents: List[str]    # intenciones más frecuentes
    orders_by_status: dict              # {"pending": 5, "confirmed": 3, ...}
