from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.application.use_cases import (
    GetPricingHistory,
    GetEnrichmentHistory,
    GetBookSummary,
    GetAuditEvents,
)
from app.domain.schemas import (
    AuditEventResponse,
    PricingHistoryItem,
    EnrichmentHistoryItem,
    BookSummaryResponse,
)
from app.infrastructure.database import get_audit_db, get_pricing_db, get_enrichment_db

router = APIRouter(prefix="/audit", tags=["audit"])


@router.get("/pricing/{book_reference}", response_model=List[PricingHistoryItem])
def get_pricing_history(
    book_reference: str,
    pricing_db: Session = Depends(get_pricing_db),
):
    try:
        return GetPricingHistory(pricing_db).execute(book_reference)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/enrichment/{book_reference}", response_model=List[EnrichmentHistoryItem])
def get_enrichment_history(
    book_reference: str,
    enrichment_db: Session = Depends(get_enrichment_db),
):
    try:
        return GetEnrichmentHistory(enrichment_db).execute(book_reference)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/summary/{book_reference}", response_model=BookSummaryResponse)
def get_book_summary(
    book_reference: str,
    pricing_db: Session = Depends(get_pricing_db),
    enrichment_db: Session = Depends(get_enrichment_db),
):
    try:
        return GetBookSummary(pricing_db, enrichment_db).execute(book_reference)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/events", response_model=List[AuditEventResponse])
def get_audit_events(
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None,
    audit_db: Session = Depends(get_audit_db),
):
    try:
        return GetAuditEvents(audit_db).execute(from_date, to_date)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
