import os
import httpx
from dotenv import load_dotenv

load_dotenv()

ORDER_URL = os.getenv("ORDER_URL", "http://order-service:8011")


class OrderClient:
    """Adapter dedicado para hablar con order-service."""

    async def create_order(self, order_data: dict, token: str | None = None) -> dict:
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.post(f"{ORDER_URL}/orders", json=order_data, headers=headers)
            response.raise_for_status()
            return response.json()

    async def get_order(self, order_id: str, token: str | None = None) -> dict:
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.get(f"{ORDER_URL}/orders/{order_id}", headers=headers)
            response.raise_for_status()
            return response.json()

    async def list_orders(self, customer_id: str | None = None, page: int = 1, page_size: int = 20, token: str | None = None) -> dict:
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        params = {"page": page, "page_size": page_size}
        if customer_id:
            params["customer_id"] = customer_id
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.get(f"{ORDER_URL}/orders", params=params, headers=headers)
            response.raise_for_status()
            return response.json()

    async def update_status(self, order_id: str, new_status: str, token: str | None = None) -> dict:
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.put(
                f"{ORDER_URL}/orders/{order_id}/status",
                json={"status": new_status},
                headers=headers,
            )
            response.raise_for_status()
            return response.json()
