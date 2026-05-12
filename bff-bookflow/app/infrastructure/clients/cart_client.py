import os
import httpx
from dotenv import load_dotenv

load_dotenv()

CART_URL = os.getenv("CART_URL", "http://cart-service:8010")


class CartClient:
    """Adapter dedicado para hablar con cart-service."""

    async def add_item(self, customer_id: str, item: dict, token: str | None = None) -> dict:
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        async with httpx.AsyncClient(timeout=15) as client:
            payload = {"customer_id": customer_id, **item}
            response = await client.post(f"{CART_URL}/cart/items", json=payload, headers=headers)
            response.raise_for_status()
            return response.json()

    async def get_cart(self, customer_id: str, token: str | None = None) -> dict:
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.get(f"{CART_URL}/cart/{customer_id}", headers=headers)
            response.raise_for_status()
            return response.json()

    async def update_item(self, item_id: str, item_data: dict, token: str | None = None) -> dict:
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.put(f"{CART_URL}/cart/items/{item_id}", json=item_data, headers=headers)
            response.raise_for_status()
            return response.json()

    async def delete_item(self, item_id: str, token: str | None = None) -> dict:
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.delete(f"{CART_URL}/cart/items/{item_id}", headers=headers)
            response.raise_for_status()
            return response.json() if response.content else {"deleted": True, "id": item_id}
