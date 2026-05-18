from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from app.infrastructure.models import (
    AuditEventModel,
    PricingDecisionReadModel,
    EnrichmentRequestReadModel,
    EnrichmentResultReadModel,
)
from app.domain.schemas import (
    AuditEventResponse,
    PricingHistoryItem,
    EnrichmentHistoryItem,
    BookSummaryResponse,
)


class GetPricingHistory:
    def __init__(self, pricing_db: Session):
        self.pricing_db = pricing_db

    def execute(self, book_reference: str) -> List[PricingHistoryItem]:
        rows = (
            self.pricing_db.query(PricingDecisionReadModel)
            .filter(PricingDecisionReadModel.book_reference == book_reference)
            .order_by(PricingDecisionReadModel.created_at.desc())
            .all()
        )
        return [
            PricingHistoryItem(
                id=row.id,
                book_reference=row.book_reference,
                suggested_price=row.suggested_price,
                explanation=row.explanation,
                condition_factor=row.condition_factor,
                source_used=None,
                timestamp=row.created_at or datetime.utcnow(),
            )
            for row in rows
        ]


class GetEnrichmentHistory:
    def __init__(self, enrichment_db: Session):
        self.enrichment_db = enrichment_db

    def execute(self, book_reference: str) -> List[EnrichmentHistoryItem]:
        requests = (
            self.enrichment_db.query(EnrichmentRequestReadModel)
            .filter(EnrichmentRequestReadModel.book_reference == book_reference)
            .order_by(EnrichmentRequestReadModel.requested_at.desc())
            .all()
        )
        result = []
        for req in requests:
            res = (
                self.enrichment_db.query(EnrichmentResultReadModel)
                .filter(EnrichmentResultReadModel.request_id == req.id)
                .first()
            )
            result.append(
                EnrichmentHistoryItem(
                    id=req.id,
                    book_reference=req.book_reference,
                    source_used=req.source_used,
                    status=req.status,
                    normalized_title=res.normalized_title if res else None,
                    normalized_author=res.normalized_author if res else None,
                    timestamp=req.requested_at or datetime.utcnow(),
                )
            )
        return result


class GetBookSummary:
    def __init__(self, pricing_db: Session, enrichment_db: Session):
        self.pricing_db = pricing_db
        self.enrichment_db = enrichment_db

    def execute(self, book_reference: str) -> BookSummaryResponse:
        pricing = GetPricingHistory(self.pricing_db).execute(book_reference)
        enrichment = GetEnrichmentHistory(self.enrichment_db).execute(book_reference)
        return BookSummaryResponse(
            book_reference=book_reference,
            pricing_history=pricing,
            enrichment_history=enrichment,
            total_pricing_decisions=len(pricing),
            total_enrichments=len(enrichment),
        )


class GetAuditEvents:
    def __init__(self, audit_db: Session):
        self.audit_db = audit_db

    def execute(self, from_date: Optional[datetime], to_date: Optional[datetime]) -> List[AuditEventResponse]:
        query = self.audit_db.query(AuditEventModel)
        if from_date:
            query = query.filter(AuditEventModel.timestamp >= from_date)
        if to_date:
            query = query.filter(AuditEventModel.timestamp <= to_date)
        rows = query.order_by(AuditEventModel.timestamp.desc()).all()
        return [
            AuditEventResponse(
                id=row.id,
                event_type=row.event_type,
                book_reference=row.book_reference,
                timestamp=row.timestamp,
                actor=row.actor,
                details=row.details,
            )
            for row in rows
        ]
