from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from app.infrastructure.clients.inventory_client import InventoryClient
from app.application.auth_middleware import validate_jwt

router = APIRouter(prefix="/api/inventory", tags=["inventory"])


@router.post("/upload")
async def upload_inventory(
    file: UploadFile = File(...),
    payload: dict = Depends(validate_jwt),
):
    try:
        client = InventoryClient()
        file_bytes = await file.read()
        return await client.upload_file(file_bytes, file.filename)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/batches")
async def get_batches(
    page: int = 1,
    page_size: int = 20,
    payload: dict = Depends(validate_jwt),
):
    try:
        client = InventoryClient()
        return await client.get_batches(page, page_size)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/batches/{batch_id}")
async def get_batch(
    batch_id: str,
    payload: dict = Depends(validate_jwt),
):
    try:
        client = InventoryClient()
        return await client.get_batch_by_id(batch_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Batch not found")


@router.get("/batches/{batch_id}/errors")
async def get_batch_errors(
    batch_id: str,
    error_type: Optional[str] = None,
    payload: dict = Depends(validate_jwt),
):
    try:
        client = InventoryClient()
        return await client.get_batch_errors(batch_id, error_type)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Batch not found")


@router.get("/batches/{batch_id}/summary")
async def get_batch_summary(
    batch_id: str,
    payload: dict = Depends(validate_jwt),
):
    try:
        client = InventoryClient()
        return await client.get_batch_summary(batch_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Batch not found")
