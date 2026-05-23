content = """import os
from decimal import Decimal
import httpx

class PricingClient:
    def __init__(self):
        self.base_url = os.getenv("PRICING_URL", "http://pricing-service:8008")

    def get_current_price(self, book_id: str) -> Decimal:
        try:
            response = httpx.get(
                f"{self.base_url}/pricing/decisions/{book_id}",
                timeout=5,
            )
            if response.status_code == 404:
                return Decimal("25000.00")  # Precio por defecto
            response.raise_for_status()
            data = response.json()
            price = (
                data.get("suggested_price")
                or data.get("final_price")
                or data.get("price")
                or data.get("unit_price")
            )
            if price is None:
                return Decimal("25000.00")
            return Decimal(str(price))
        except Exception:
            return Decimal("25000.00")  # Fallback siempre
"""
with open("cart-service/app/infrastructure/clients/pricing_client.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Done")
