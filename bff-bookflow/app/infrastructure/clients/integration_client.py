import os
import httpx
from dotenv import load_dotenv

load_dotenv()
INTEGRATION_URL = os.getenv('INTEGRATION_URL', 'http://integration-service:8008')


class IntegrationClient:
    async def trigger(self, batch_id: str) -> dict:
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.post(f'{INTEGRATION_URL}/integration/trigger/{batch_id}')
            r.raise_for_status()
            return r.json()

    async def external_health(self) -> dict:
        async with httpx.AsyncClient(timeout=5) as client:
            r = await client.get(f'{INTEGRATION_URL}/external/health')
            r.raise_for_status()
            return r.json()
