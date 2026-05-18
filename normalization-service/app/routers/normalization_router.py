from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.domain.schemas import EnrichmentResultInput, NormalizedRecordResponse, BatchInput, BatchResponse
from app.infrastructure.repositories import NormalizedRecordRepositoryPostgres
from app.infrastructure.database import get_db, get_catalog_db
from app.domain.duplicate_detector import DuplicateDetector
from app.application.use_cases import NormalizeRecord, NormalizeBatch, GetRecords

router = APIRouter(prefix="/normalization", tags=["normalization"])


@router.post("/normalize", response_model=NormalizedRecordResponse, status_code=201)
def normalize_record(
    input_data: EnrichmentResultInput,
    db: Session = Depends(get_db),
    catalog_db: Session = Depends(get_catalog_db),
):
    try:
        repository = NormalizedRecordRepositoryPostgres(db)
        detector = DuplicateDetector(catalog_db)
        use_case = NormalizeRecord(repository, detector)
        record = use_case.execute(input_data)
        return NormalizedRecordResponse(
            id=record.id,
            enrichment_result_id=record.enrichment_result_id,
            normalized_title=record.normalized_title,
            normalized_author=record.normalized_author,
            normalized_isbn=record.normalized_isbn,
            isbn_valid=record.isbn_valid,
            issn_valid=record.issn_valid,
            is_duplicate=record.is_duplicate,
            duplicate_of_id=record.duplicate_of_id,
            created_at=record.created_at,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/batch", response_model=BatchResponse, status_code=201)
def normalize_batch(
    batch: BatchInput,
    db: Session = Depends(get_db),
    catalog_db: Session = Depends(get_catalog_db),
):
    try:
        repository = NormalizedRecordRepositoryPostgres(db)
        detector = DuplicateDetector(catalog_db)
        use_case = NormalizeBatch(repository, detector)
        records = use_case.execute(batch.records)
        return BatchResponse(
            processed=len(records),
            results=[
                NormalizedRecordResponse(
                    id=r.id,
                    enrichment_result_id=r.enrichment_result_id,
                    normalized_title=r.normalized_title,
                    normalized_author=r.normalized_author,
                    normalized_isbn=r.normalized_isbn,
                    isbn_valid=r.isbn_valid,
                    issn_valid=r.issn_valid,
                    is_duplicate=r.is_duplicate,
                    duplicate_of_id=r.duplicate_of_id,
                    created_at=r.created_at,
                ) for r in records
            ]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/records", response_model=List[NormalizedRecordResponse])
def get_records(
    db: Session = Depends(get_db),
    catalog_db: Session = Depends(get_catalog_db),
):
    try:
        repository = NormalizedRecordRepositoryPostgres(db)
        detector = DuplicateDetector(catalog_db)
        use_case = GetRecords(repository)
        records = use_case.execute()
        return [
            NormalizedRecordResponse(
                id=r.id,
                enrichment_result_id=r.enrichment_result_id,
                normalized_title=r.normalized_title,
                normalized_author=r.normalized_author,
                normalized_isbn=r.normalized_isbn,
                isbn_valid=r.isbn_valid,
                issn_valid=r.issn_valid,
                is_duplicate=r.is_duplicate,
                duplicate_of_id=r.duplicate_of_id,
                created_at=r.created_at,
            ) for r in records
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
def health():
    return {"status": "ok", "service": "normalization-service"}
