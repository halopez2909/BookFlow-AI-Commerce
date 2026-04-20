from fastapi import APIRouter, Depends, HTTPException
from app.infrastructure.clients.pricing_client import PricingClient
from app.application.auth_middleware import validate_jwt

router = APIRouter(prefix='/api/pricing', tags=['pricing'])


@router.post('/calculate', status_code=201)
async def calculate_price(data: dict, payload: dict = Depends(validate_jwt)):
    try:
        client = PricingClient()
        return await client.calculate(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/decisions/{book_reference}')
async def get_pricing_decision(book_reference: str, payload: dict = Depends(validate_jwt)):
    try:
        client = PricingClient()
        return await client.get_decision(book_reference)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
