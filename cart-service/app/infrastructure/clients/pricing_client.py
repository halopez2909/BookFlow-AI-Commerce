import os
from decimal import Decimal

import httpx


class PricingClient:

    def __init__(self):
        self.base_url = os.getenv("PRICING_URL", "http://localhost:8005")

    def get_current_price(self, book_id: str) -> Decimal:
        """
        Consulta Pricing Service.
        Endpoint esperado:
        GET /pricing/decisions/{book_reference}

        Respuestas esperadas posibles:
        {
          "book_reference": "1",
          "suggested_price": 45000
        }

        También acepta:
        {
          "price": 45000
        }
        """
        try:
            response = httpx.get(
                f"{self.base_url}/pricing/decisions/{book_id}",
                timeout=5,
            )

            response.raise_for_status()
            data = response.json()

            price = (
                data.get("suggested_price")
                or data.get("final_price")
                or data.get("price")
                or data.get("unit_price")
            )

            if price is None:
                raise ValueError("Pricing Service no retornó precio.")

            return Decimal(str(price))

        except httpx.RequestError:
            # Fallback temporal para pruebas locales cuando Pricing Service no está levantado.
            # En integración real, PRICING_URL debe apuntar al servicio real.
            return Decimal("50000.00")
