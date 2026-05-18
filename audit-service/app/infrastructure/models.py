import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, JSON, Float, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# ──────────────────────────────────────────
# Tabla propia del audit-service (audit_db)
# ──────────────────────────────────────────

class AuditEventModel(Base):
    __tablename__ = "audit_events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_type = Column(String, nullable=False, index=True)
    book_reference = Column(String, nullable=False, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    actor = Column(String, nullable=False, default="system")
    details = Column(JSON, nullable=True)


# ──────────────────────────────────────────
# Solo lectura — pricing_db (Sprint 2)
# ──────────────────────────────────────────

class PricingDecisionReadModel(Base):
    __tablename__ = "pricing_decisions"

    id = Column(UUID(as_uuid=True), primary_key=True)
    book_reference = Column(String, nullable=False)
    suggested_price = Column(Float, nullable=True)
    explanation = Column(String, nullable=True)
    condition_factor = Column(Float, nullable=True)
    reference_count = Column(Float, nullable=True)
    created_at = Column(DateTime, nullable=True)


# ──────────────────────────────────────────
# Solo lectura — enrichment_db (Sprint 2)
# ──────────────────────────────────────────

class EnrichmentRequestReadModel(Base):
    __tablename__ = "enrichment_requests"

    id = Column(UUID(as_uuid=True), primary_key=True)
    book_reference = Column(String, nullable=False)
    status = Column(String, nullable=True)
    source_used = Column(String, nullable=True)
    requested_at = Column(DateTime, nullable=True)


class EnrichmentResultReadModel(Base):
    __tablename__ = "enrichment_results"

    id = Column(UUID(as_uuid=True), primary_key=True)
    request_id = Column(UUID(as_uuid=True), nullable=False)
    normalized_title = Column(String, nullable=True)
    normalized_author = Column(String, nullable=True)


# ──────────────────────────────────────────
# Solo lectura — order_db (Sprint 3)
# Modelos de Cart y Order que crea ALEJO y ANDRES
# ──────────────────────────────────────────

class CartReadModel(Base):
    __tablename__ = "carts"

    id = Column(UUID(as_uuid=True), primary_key=True)
    customer_id = Column(String, nullable=False, index=True)
    status = Column(String, nullable=True)          # active, cleared, converted
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)


class CartItemReadModel(Base):
    __tablename__ = "cart_items"

    id = Column(UUID(as_uuid=True), primary_key=True)
    cart_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    book_id = Column(String, nullable=False)
    quantity = Column(Integer, nullable=True)
    unit_price = Column(Float, nullable=True)


class OrderReadModel(Base):
    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), primary_key=True)
    customer_id = Column(String, nullable=False, index=True)
    status = Column(String, nullable=True)          # pending, confirmed, shipped, delivered, cancelled
    total_amount = Column(Float, nullable=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)


class OrderItemReadModel(Base):
    __tablename__ = "order_items"

    id = Column(UUID(as_uuid=True), primary_key=True)
    order_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    book_id = Column(String, nullable=False)
    quantity = Column(Integer, nullable=True)
    unit_price = Column(Float, nullable=True)


# ──────────────────────────────────────────
# Solo lectura — assistant_db (Sprint 3)
# Modelo de AssistantInteraction que crea JUANSE
# ──────────────────────────────────────────

class AssistantInteractionReadModel(Base):
    __tablename__ = "assistant_interactions"

    id = Column(UUID(as_uuid=True), primary_key=True)
    session_id = Column(String, nullable=False, index=True)
    user_question = Column(String, nullable=True)
    interpreted_intent = Column(String, nullable=True)
    answer_text = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=True)
