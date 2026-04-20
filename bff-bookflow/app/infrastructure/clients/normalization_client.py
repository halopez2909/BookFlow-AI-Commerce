import os
import httpx
from dotenv import load_dotenv

load_dotenv()
NORMALIZATION_URL = os.getenv('NORMALIZATION_URL', 'http://normalization-service:8005')


class NormalizationClient:
    async def normalize(self, data: dict) -> dict:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.post(f'{NORMALIZATION_URL}/normalization/normalize', json=data)
            r.raise_for_status()
            return r.json()

    async def normalize_batch(self, records: list) -> dict:
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.post(f'{NORMALIZATION_URL}/normalization/batch', json={'records': records})
            r.raise_for_status()
            return r.json()

    async def get_records(self) -> list:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(f'{NORMALIZATION_URL}/normalization/records')
            r.raise_for_status()
            return r.json()

    async def health(self) -> dict:
        async with httpx.AsyncClient(timeout=5) as client:
            r = await client.get(f'{NORMALIZATION_URL}/health')
            r.raise_for_status()
            return r.json()
