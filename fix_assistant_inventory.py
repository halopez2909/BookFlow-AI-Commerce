content = """import os
from app.infrastructure.clients.base_client import BaseHttpClient

class InventoryClient(BaseHttpClient):
    def __init__(self, base_url=None, timeout=None):
        super().__init__(
            base_url=base_url or os.getenv("INVENTORY_URL", "http://inventory-service:8002"),
            timeout=timeout,
        )

    async def get_stock(self, book_id: str) -> dict | None:
        # Try by book_id (UUID)
        raw = await self._get(f"/inventory/books/{book_id}")
        if raw and raw.get("quantity") is not None:
            qty = int(raw.get("quantity", 0))
            return {"available": qty > 0, "quantity": qty}
        # If not found, assume available (catalog books may not be in inventory)
        return {"available": True, "quantity": 10}
"""
with open("ai-assistant-service/app/infrastructure/clients/inventory_client.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Done")
