import uuid
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.domain.schemas import (
    EnrichBookRequest,
    EnrichmentResultResponse,
    EnrichmentRequestResponse,
)
from app.application.use_cases import (
    EnrichBook,
    GetEnrichmentRequest,
    GetEnrichmentRequestsByBookReference,
)
from app.infrastructure.repositories import (
    EnrichmentRequestRepositoryPostgres,
    EnrichmentResultRepositoryPostgres,
)
from app.infrastructure.providers.factory import EnrichmentProviderFactory
from app.infrastructure.database import get_db

router = APIRouter(prefix="/enrichment", tags=["enrichment"])


def get_enrich_use_case(db: Session = Depends(get_db)) -> EnrichBook:
    return EnrichBook(
        provider=EnrichmentProviderFactory.get_provider(),
        request_repo=EnrichmentRequestRepositoryPostgres(db),
        result_repo=EnrichmentResultRepositoryPostgres(db),
    )


def get_request_use_case(db: Session = Depends(get_db)) -> GetEnrichmentRequest:
    return GetEnrichmentRequest(EnrichmentRequestRepositoryPostgres(db))


def get_requests_by_book_reference_use_case(
    db: Session = Depends(get_db),
) -> GetEnrichmentRequestsByBookReference:
    return GetEnrichmentRequestsByBookReference(
        EnrichmentRequestRepositoryPostgres(db)
    )


@router.post("/enrich", response_model=EnrichmentResultResponse, status_code=status.HTTP_201_CREATED)
async def enrich_book(
    request: EnrichBookRequest,
    use_case: EnrichBook = Depends(get_enrich_use_case),
):
    try:
        return await use_case.execute(request)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get("/requests/{request_id}", response_model=EnrichmentRequestResponse)
def get_request(
    request_id: str,
    use_case: GetEnrichmentRequest = Depends(get_request_use_case),
):
    try:
        return use_case.execute(uuid.UUID(request_id))
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enrichment request not found",
        )


@router.get("/requests", response_model=list[EnrichmentRequestResponse])
def get_requests_by_book_reference(
    book_reference: Optional[str] = Query(default=None),
    use_case: GetEnrichmentRequestsByBookReference = Depends(
        get_requests_by_book_reference_use_case
    ),
):
    if not book_reference:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="book_reference is required",
        )

    try:
        return use_case.execute(book_reference)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )