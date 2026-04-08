import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class EnrichmentRequestModel(Base):
    __tablename__ = "enrichment_requests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    book_reference = Column(String, nullable=False, index=True)
    title = Column(String, nullable=True)
    author = Column(String, nullable=True)
    isbn = Column(String, nullable=True)
    status = Column(String, nullable=False, default="pending")
    requested_at = Column(DateTime, default=datetime.utcnow)
    source_used = Column(String, nullable=True)


class EnrichmentResultModel(Base):
    __tablename__ = "enrichment_results"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    request_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    normalized_title = Column(String, nullable=True)
    normalized_author = Column(String, nullable=True)
    normalized_publisher = Column(String, nullable=True)
    normalized_description = Column(String, nullable=True)
    cover_url = Column(String, nullable=True)
    metadata_json = Column(JSON, nullable=True)
