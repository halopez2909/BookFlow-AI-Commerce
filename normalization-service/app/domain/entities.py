from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import uuid


@dataclass(frozen=True)
class NormalizedRecord:
    id: str
    enrichment_result_id: str
    normalized_title: str
    normalized_author: str
    normalized_isbn: Optional[str]
    isbn_valid: bool
    issn_valid: bool
    is_duplicate: bool
    duplicate_of_id: Optional[str]
    created_at: datetime

    @staticmethod
    def create(
        enrichment_result_id: str,
        normalized_title: str,
        normalized_author: str,
        normalized_isbn: Optional[str] = None,
        isbn_valid: bool = True,
        issn_valid: bool = True,
        is_duplicate: bool = False,
        duplicate_of_id: Optional[str] = None,
    ) -> 'NormalizedRecord':
        return NormalizedRecord(
            id=str(uuid.uuid4()),
            enrichment_result_id=enrichment_result_id,
            normalized_title=normalized_title,
            normalized_author=normalized_author,
            normalized_isbn=normalized_isbn,
            isbn_valid=isbn_valid,
            issn_valid=issn_valid,
            is_duplicate=is_duplicate,
            duplicate_of_id=duplicate_of_id,
            created_at=datetime.utcnow(),
        )
