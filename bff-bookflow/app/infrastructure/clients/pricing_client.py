import os
import httpx
from dotenv import load_dotenv

load_dotenv()

PRICING_URL = os.getenv("PRICING_URL", "http://pricing-service:8008")


class PricingClient:
    """Adapter dedicado para hablar con pricing-service."""

    async def get_decision(self, book_id: str) -> dict:
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.get(f"{PRICING_URL}/pricing/decisions/{book_id}")
            response.raise_for_status()
            return response.json()
