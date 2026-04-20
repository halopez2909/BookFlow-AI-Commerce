import os
import httpx
from dotenv import load_dotenv

load_dotenv()
PRICING_URL = os.getenv('PRICING_URL', 'http://pricing-service:8006')


class PricingClient:
    async def calculate(self, data: dict) -> dict:
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.post(f'{PRICING_URL}/pricing/calculate', json=data)
            r.raise_for_status()
            return r.json()

    async def get_decision(self, book_reference: str) -> dict:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(f'{PRICING_URL}/pricing/decisions/{book_reference}')
            r.raise_for_status()
            return r.json()

    async def health(self) -> dict:
        async with httpx.AsyncClient(timeout=5) as client:
            r = await client.get(f'{PRICING_URL}/health')
            r.raise_for_status()
            return r.json()
