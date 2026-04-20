from fastapi import APIRouter, Depends, HTTPException
from app.infrastructure.clients.normalization_client import NormalizationClient
from app.application.auth_middleware import validate_jwt

router = APIRouter(prefix='/api/normalization', tags=['normalization'])


@router.post('/normalize', status_code=201)
async def normalize(data: dict, payload: dict = Depends(validate_jwt)):
    try:
        client = NormalizationClient()
        return await client.normalize(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/batch', status_code=201)
async def normalize_batch(data: dict, payload: dict = Depends(validate_jwt)):
    try:
        client = NormalizationClient()
        return await client.normalize_batch(data.get('records', []))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/records')
async def get_records(payload: dict = Depends(validate_jwt)):
    try:
        client = NormalizationClient()
        return await client.get_records()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
