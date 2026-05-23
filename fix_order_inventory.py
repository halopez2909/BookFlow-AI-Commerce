content = """import os
import httpx
from dotenv import load_dotenv

load_dotenv()

INVENTORY_URL = os.getenv("INVENTORY_URL", "http://inventory-service:8002")


class InventoryClient:

    async def check_availability(self, book_id: str, quantity: int) -> bool:
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                r = await client.get(f"{INVENTORY_URL}/inventory/books/{book_id}")
                if r.status_code == 404:
                    # Libro no en inventario legacy - permitir compra
                    return True
                if r.status_code != 200:
                    return True  # Fallback permisivo
                data = r.json()
                available = data.get("quantity", 0)
                return available >= quantity
        except Exception:
            return True  # Fallback permisivo

    async def deduct_stock(self, book_id: str, quantity: int) -> bool:
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                r = await client.post(
                    f"{INVENTORY_URL}/inventory/books/{book_id}/deduct",
                    json={"quantity": quantity}
                )
                return r.status_code in [200, 201, 404]  # 404 = no en inventario, OK
        except Exception:
            return True

    async def restore_stock(self, book_id: str, quantity: int) -> bool:
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                r = await client.post(
                    f"{INVENTORY_URL}/inventory/books/{book_id}/restore",
                    json={"quantity": quantity}
                )
                return r.status_code in [200, 201, 404]
        except Exception:
            return True
"""
with open("order-service/app/infrastructure/clients/inventory_client.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Done")
