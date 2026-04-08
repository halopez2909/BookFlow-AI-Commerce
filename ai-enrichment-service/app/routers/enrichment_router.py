import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.domain.schemas import EnrichBookRequest, EnrichmentResultResponse, EnrichmentRequestResponse
from app.application.use_cases import EnrichBook, GetEnrichmentRequest
from app.infrastructure.repositories import EnrichmentRequestRepositoryPostgres, EnrichmentResultRepositoryPostgres
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


@router.post("/enrich", response_model=EnrichmentResultResponse, status_code=status.HTTP_201_CREATED)
async def enrich_book(
    request: EnrichBookRequest,
    use_case: EnrichBook = Depends(get_enrich_use_case),
):
    try:
        return await use_case.execute(request)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/requests/{request_id}", response_model=EnrichmentRequestResponse)
def get_request(
    request_id: str,
    use_case: GetEnrichmentRequest = Depends(get_request_use_case),
):
    try:
        return use_case.execute(uuid.UUID(request_id))
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Enrichment request not found")
