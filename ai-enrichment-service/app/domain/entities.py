import uuid
from datetime import datetime
from typing import Optional
from enum import Enum


class EnrichmentStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


class EnrichmentRequest:
    def __init__(
        self,
        id: uuid.UUID,
        book_reference: str,
        title: Optional[str],
        author: Optional[str],
        isbn: Optional[str],
        status: EnrichmentStatus,
        requested_at: datetime,
        source_used: Optional[str] = None,
    ):
        self.id = id
        self.book_reference = book_reference
        self.title = title
        self.author = author
        self.isbn = isbn
        self.status = status
        self.requested_at = requested_at
        self.source_used = source_used


class EnrichmentResult:
    def __init__(
        self,
        id: uuid.UUID,
        request_id: uuid.UUID,
        normalized_title: Optional[str],
        normalized_author: Optional[str],
        normalized_publisher: Optional[str],
        normalized_description: Optional[str],
        cover_url: Optional[str],
        metadata_json: Optional[dict],
    ):
        self.id = id
        self.request_id = request_id
        self.normalized_title = normalized_title
        self.normalized_author = normalized_author
        self.normalized_publisher = normalized_publisher
        self.normalized_description = normalized_description
        self.cover_url = cover_url
        self.metadata_json = metadata_json
