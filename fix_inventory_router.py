new_router = """import os
import uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from app.domain.schemas import ImportBatchResponse
from app.application.use_cases import ProcessInventoryFile, GetBatches, GetBatchById
from app.infrastructure.repositories import InventoryRepositoryPostgres, ImportBatchRepositoryPostgres, ImportErrorRepositoryPostgres
from app.infrastructure.database import get_db
from app.infrastructure.models import InventoryItemModel
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()
MAX_FILE_SIZE_MB = int(os.getenv("INVENTORY_MAX_FILE_SIZE_MB", 10))
router = APIRouter(prefix="/inventory", tags=["inventory"])

class StockAdjustRequest(BaseModel):
    quantity: int

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
        raise HTTPException(status_code=400, detail="File format not supported. Use .xls, .xlsx or .csv")
    file_bytes = await file.read()
    size_mb = len(file_bytes) / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        raise HTTPException(status_code=400, detail=f"File size exceeds the maximum allowed ({MAX_FILE_SIZE_MB} MB)")
    if len(file_bytes) == 0:
        raise HTTPException(status_code=400, detail="File is empty")
    try:
        return use_case.execute(file_bytes, file.filename)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/batches", response_model=dict)
def get_batches(page: int = 1, page_size: int = 20, use_case: GetBatches = Depends(get_batches_use_case)):
    items, total = use_case.execute(page, page_size)
    return {"items": items, "total": total, "page": page, "page_size": page_size}

@router.get("/batches/{batch_id}", response_model=ImportBatchResponse)
def get_batch(batch_id: str, use_case: GetBatchById = Depends(get_batch_by_id_use_case)):
    try:
        return use_case.execute(uuid.UUID(batch_id))
    except ValueError as e:
        if "BATCH_NOT_FOUND" in str(e):
            raise HTTPException(status_code=404, detail="Batch not found")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/books/{book_id}")
def get_book_stock(book_id: str, db: Session = Depends(get_db)):
    item = db.query(InventoryItemModel).filter(
        InventoryItemModel.book_reference == book_id
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="Libro no encontrado en inventario")
    return {
        "book_id": book_id,
        "quantity": item.quantity_available,
        "condition": item.condition,
        "quantity_reserved": item.quantity_reserved,
    }

@router.post("/books/{book_id}/deduct")
def deduct_stock(book_id: str, request: StockAdjustRequest, db: Session = Depends(get_db)):
    item = db.query(InventoryItemModel).filter(
        InventoryItemModel.book_reference == book_id
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="Libro no encontrado en inventario")
    if item.quantity_available < request.quantity:
        raise HTTPException(status_code=409, detail="Stock insuficiente")
    item.quantity_available -= request.quantity
    db.commit()
    return {"book_id": book_id, "quantity_available": item.quantity_available}

@router.post("/books/{book_id}/restore")
def restore_stock(book_id: str, request: StockAdjustRequest, db: Session = Depends(get_db)):
    item = db.query(InventoryItemModel).filter(
        InventoryItemModel.book_reference == book_id
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="Libro no encontrado en inventario")
    item.quantity_available += request.quantity
    db.commit()
    return {"book_id": book_id, "quantity_available": item.quantity_available}
"""

with open("inventory-service/app/routers/inventory_router.py", "w", encoding="utf-8") as f:
    f.write(new_router)
print("Done")
