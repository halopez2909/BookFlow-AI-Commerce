import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from typing import List
from app.domain.schemas import ImportBatchResponse
from app.application.use_cases import ProcessInventoryFile, GetBatches, GetBatchById
from app.infrastructure.repositories import InventoryRepositoryPostgres, ImportBatchRepositoryPostgres, ImportErrorRepositoryPostgres
from app.infrastructure.database import get_db
from dotenv import load_dotenv

load_dotenv()

MAX_FILE_SIZE_MB = int(os.getenv("INVENTORY_MAX_FILE_SIZE_MB", 10))

router = APIRouter(prefix="/inventory", tags=["inventory"])


def get_process_use_case(db: Session = Depends(get_db)) -> ProcessInventoryFile:
    return ProcessInventoryFile(
        inventory_repo=InventoryRepositoryPostgres(db),
        batch_repo=ImportBatchRepositoryPostgres(db),
        error_repo=ImportErrorRepositoryPostgres(db),
    )


def get_batches_use_case(db: Session = Depends(get_db)) -> GetBatches:
    return GetBatches(ImportBatchRepositoryPostgres(db))


def get_batch_by_id_use_case(db: Session = Depends(get_db)) -> GetBatchById:
    return GetBatchById(ImportBatchRepositoryPostgres(db))


@router.post("/upload", response_model=ImportBatchResponse, status_code=status.HTTP_201_CREATED)
async def upload_inventory(
    file: UploadFile = File(...),
    use_case: ProcessInventoryFile = Depends(get_process_use_case),
):
    allowed_extensions = ["xls", "xlsx", "csv"]
    extension = file.filename.split(".")[-1].lower()
    if extension not in allowed_extensions:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File format not supported. Use .xls, .xlsx or .csv")

    file_bytes = await file.read()
    size_mb = len(file_bytes) / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"File size exceeds the maximum allowed ({MAX_FILE_SIZE_MB} MB)")

    if len(file_bytes) == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File is empty")

    try:
        return use_case.execute(file_bytes, file.filename)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/batches", response_model=dict)
def get_batches(
    page: int = 1,
    page_size: int = 20,
    use_case: GetBatches = Depends(get_batches_use_case),
):
    items, total = use_case.execute(page, page_size)
    return {"items": items, "total": total, "page": page, "page_size": page_size}


@router.get("/batches/{batch_id}", response_model=ImportBatchResponse)
def get_batch(
    batch_id: str,
    use_case: GetBatchById = Depends(get_batch_by_id_use_case),
):
    try:
        import uuid
        return use_case.execute(uuid.UUID(batch_id))
    except ValueError as e:
        if "BATCH_NOT_FOUND" in str(e):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Batch not found")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
