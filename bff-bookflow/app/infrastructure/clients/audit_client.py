import os
import httpx
from dotenv import load_dotenv

load_dotenv()
AUDIT_URL = os.getenv('AUDIT_URL', 'http://audit-service:8007')


class AuditClient:
    async def get_summary(self, book_reference: str) -> dict:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(f'{AUDIT_URL}/audit/summary/{book_reference}')
            r.raise_for_status()
            return r.json()

    async def get_pricing_audit(self, book_reference: str) -> dict:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(f'{AUDIT_URL}/audit/pricing/{book_reference}')
            r.raise_for_status()
            return r.json()

    async def get_enrichment_audit(self, book_reference: str) -> dict:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(f'{AUDIT_URL}/audit/enrichment/{book_reference}')
            r.raise_for_status()
            return r.json()

    async def health(self) -> dict:
        async with httpx.AsyncClient(timeout=5) as client:
            r = await client.get(f'{AUDIT_URL}/health')
            r.raise_for_status()
            return r.json()
