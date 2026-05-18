"""
InventoryClient: Adapter del Inventory Service. Consulta stock real
por book_id. Si el endpoint no existe o devuelve 404, retorna None
y el ResponseBuilder lo interpreta como 'no se pudo confirmar stock'.
"""
import os

from app.infrastructure.clients.base_client import BaseHttpClient


class InventoryClient(BaseHttpClient):
    def __init__(self, base_url: str | None = None, timeout: float | None = None) -> None:
        super().__init__(
            base_url=base_url or os.getenv("INVENTORY_URL", "http://inventory-service:8002"),
            timeout=timeout,
        )

    async def get_stock(self, book_id: str) -> dict | None:
        """
        Devuelve {'available': bool, 'quantity': int} o None si no se
        puede determinar. Soporta el endpoint estándar /inventory/items/{id}.
        """
        raw = await self._get(f"/inventory/items/{book_id}")
        if not raw:
            return None
        qty = raw.get("quantity_available", raw.get("quantity", 0)) or 0
        return {
            "available": qty > 0,
            "quantity": int(qty),
        }