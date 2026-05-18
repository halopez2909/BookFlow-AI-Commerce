import os
import httpx


class InventoryClient:

    def __init__(self):
        self.base_url = os.getenv("INVENTORY_URL", "http://localhost:8003")

    def check_availability(self, book_id: str, quantity: int) -> bool:
        """
        Consulta Inventory Service.
        Endpoint esperado:
        GET /inventory/items/{book_id}

        Respuestas esperadas posibles:
        {
          "book_id": "1",
          "quantity_available": 10
        }

        También acepta:
        {
          "stock": 10
        }
        """
        try:
            response = httpx.get(
                f"{self.base_url}/inventory/items/{book_id}",
                timeout=5,
            )

            if response.status_code == 404:
                return False

            response.raise_for_status()
            data = response.json()

            available = (
                data.get("quantity_available")
                or data.get("available_quantity")
                or data.get("stock")
                or data.get("quantity")
                or 0
            )

            return int(available) >= quantity

        except httpx.RequestError:
            # Fallback temporal para pruebas locales cuando Inventory Service no está levantado.
            # En integración real, INVENTORY_URL debe apuntar al servicio real.
            return True
