from fastapi import APIRouter, Depends, HTTPException
from app.infrastructure.clients.integration_client import IntegrationClient
from app.application.auth_middleware import validate_jwt

router = APIRouter(prefix='/api/integration', tags=['integration'])


@router.post('/trigger/{batch_id}', status_code=201)
async def trigger_integration(batch_id: str, payload: dict = Depends(validate_jwt)):
    try:
        client = IntegrationClient()
        return await client.trigger(batch_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/external/health')
async def external_health():
    try:
        client = IntegrationClient()
        return await client.external_health()
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))
