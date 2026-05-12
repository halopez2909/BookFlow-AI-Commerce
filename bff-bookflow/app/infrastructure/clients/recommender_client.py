import os
import httpx
from dotenv import load_dotenv

load_dotenv()

RECOMMENDER_URL = os.getenv("RECOMMENDER_URL", "http://recommender-service:8013")


class RecommenderClient:
    """Adapter dedicado para hablar con recommender-service."""

    async def get_recommendations(self, book_id: str, limit: int = 6) -> dict:
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.get(
                f"{RECOMMENDER_URL}/recommendations/{book_id}",
                params={"limit": limit},
            )
            response.raise_for_status()
            return response.json()

    async def get_popular(self, limit: int = 10) -> dict:
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.get(
                f"{RECOMMENDER_URL}/recommendations/popular",
                params={"limit": limit},
            )
            response.raise_for_status()
            return response.json()
