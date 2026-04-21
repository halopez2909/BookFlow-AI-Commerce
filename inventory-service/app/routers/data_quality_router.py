import uuid
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.application.use_cases import GetBatchErrors, GetBatchSummary
from app.infrastructure.repositories import ImportBatchRepositoryPostgres, ImportErrorRepositoryPostgres
from app.infrastructure.database import get_db

router = APIRouter(prefix="/inventory", tags=["data-quality"])


def get_batch_errors_use_case(db: Session = Depends(get_db)) -> GetBatchErrors:
    return GetBatchErrors(ImportErrorRepositoryPostgres(db))


def get_batch_summary_use_case(db: Session = Depends(get_db)) -> GetBatchSummary:
    return GetBatchSummary(
        batch_repo=ImportBatchRepositoryPostgres(db),
        error_repo=ImportErrorRepositoryPostgres(db),
    )


@router.get("/batches/{batch_id}/errors")
def get_batch_errors(
    batch_id: str,
    error_type: Optional[str] = None,
    use_case: GetBatchErrors = Depends(get_batch_errors_use_case),
):
    try:
        return use_case.execute(uuid.UUID(batch_id), error_type)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Batch not found")


@router.get("/batches/{batch_id}/summary")
def get_batch_summary(
    batch_id: str,
    use_case: GetBatchSummary = Depends(get_batch_summary_use_case),
):
    try:
        return use_case.execute(uuid.UUID(batch_id))
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Batch not found")
