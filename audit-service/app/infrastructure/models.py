import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, JSON, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Tabla propia del audit-service
class AuditEventModel(Base):
    __tablename__ = "audit_events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_type = Column(String, nullable=False, index=True)
    book_reference = Column(String, nullable=False, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    actor = Column(String, nullable=False, default="system")
    details = Column(JSON, nullable=True)


# --- Modelos de solo lectura desde pricing_db ---
class PricingDecisionReadModel(Base):
    __tablename__ = "pricing_decisions"

    id = Column(UUID(as_uuid=True), primary_key=True)
    book_reference = Column(String, nullable=False)
    suggested_price = Column(Float, nullable=True)
    explanation = Column(String, nullable=True)
    condition_factor = Column(Float, nullable=True)
    reference_count = Column(Float, nullable=True)
    created_at = Column(DateTime, nullable=True)


# --- Modelos de solo lectura desde enrichment_db ---
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
