"""
PricingClient: Adapter del Pricing Service. Consulta el precio
sugerido (decision) para un book_reference.
"""
import os

from app.infrastructure.clients.base_client import BaseHttpClient


class PricingClient(BaseHttpClient):
    def __init__(self, base_url: str | None = None, timeout: float | None = None) -> None:
        super().__init__(
            base_url=base_url or os.getenv("PRICING_URL", "http://pricing-service:8008"),
            timeout=timeout,
        )

    async def get_price(self, book_reference: str) -> dict | None:
        """
        Devuelve {'price': float, 'currency': str, 'explanation': str} o None.
        """
        raw = await self._get(f"/pricing/decisions/{book_reference}")
        if not raw:
            return None
        return {
            "price": raw.get("suggested_price"),
            "currency": raw.get("currency", "COP"),
            "explanation": raw.get("explanation", ""),
        }