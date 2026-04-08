import os
import httpx
from dotenv import load_dotenv

load_dotenv()

INVENTORY_URL = os.getenv("INVENTORY_URL")


class InventoryClient:

    async def upload_file(self, file_bytes: bytes, file_name: str) -> dict:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{INVENTORY_URL}/inventory/upload",
                files={"file": (file_name, file_bytes)},
            )
            response.raise_for_status()
            return response.json()

    async def get_batches(self, page: int, page_size: int) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{INVENTORY_URL}/inventory/batches", params={"page": page, "page_size": page_size})
            response.raise_for_status()
            return response.json()

    async def get_batch_by_id(self, batch_id: str) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{INVENTORY_URL}/inventory/batches/{batch_id}")
            response.raise_for_status()
            return response.json()

    async def get_batch_errors(self, batch_id: str, error_type: str = None) -> dict:
        async with httpx.AsyncClient() as client:
            params = {}
            if error_type:
                params["error_type"] = error_type
            response = await client.get(f"{INVENTORY_URL}/inventory/batches/{batch_id}/errors", params=params)
            response.raise_for_status()
            return response.json()

    async def get_batch_summary(self, batch_id: str) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{INVENTORY_URL}/inventory/batches/{batch_id}/summary")
            response.raise_for_status()
            return response.json()
