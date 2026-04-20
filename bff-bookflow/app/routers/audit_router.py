from fastapi import APIRouter, Depends, HTTPException
from app.infrastructure.clients.audit_client import AuditClient
from app.application.auth_middleware import validate_jwt

router = APIRouter(prefix='/api/audit', tags=['audit'])


@router.get('/summary/{book_reference}')
async def get_audit_summary(book_reference: str, payload: dict = Depends(validate_jwt)):
    try:
        client = AuditClient()
        return await client.get_summary(book_reference)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get('/pricing/{book_reference}')
async def get_pricing_audit(book_reference: str, payload: dict = Depends(validate_jwt)):
    try:
        client = AuditClient()
        return await client.get_pricing_audit(book_reference)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get('/enrichment/{book_reference}')
async def get_enrichment_audit(book_reference: str, payload: dict = Depends(validate_jwt)):
    try:
        client = AuditClient()
        return await client.get_enrichment_audit(book_reference)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
