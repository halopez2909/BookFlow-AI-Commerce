content = """import os
import httpx

class InventoryClient:
    def __init__(self):
        self.base_url = os.getenv("INVENTORY_URL", "http://inventory-service:8002")

    def check_availability(self, book_id: str, quantity: int) -> bool:
        try:
            response = httpx.get(
                f"{self.base_url}/inventory/books/{book_id}",
                timeout=5,
            )
            if response.status_code == 404:
                return True  # Si no esta en inventario, permitir agregar
            response.raise_for_status()
            data = response.json()
            available = (
                data.get("quantity_available")
                or data.get("quantity")
                or data.get("stock")
                or 0
            )
            return int(available) >= quantity
        except Exception:
            return True  # Fallback: permitir si no se puede verificar
"""
with open("cart-service/app/infrastructure/clients/inventory_client.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Done")
