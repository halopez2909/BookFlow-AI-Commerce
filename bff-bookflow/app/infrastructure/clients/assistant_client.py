import os
import httpx
from dotenv import load_dotenv

load_dotenv()

ASSISTANT_URL = os.getenv("ASSISTANT_URL", "http://ai-assistant-service:8012")


class AssistantClient:
    """Adapter dedicado para hablar con ai-assistant-service."""

    async def query(self, query_text: str, session_id: str | None = None, customer_id: str | None = None) -> dict:
        async with httpx.AsyncClient(timeout=30) as client:
            payload = {"query": query_text}
            if session_id:
                payload["session_id"] = session_id
            if customer_id:
                payload["customer_id"] = customer_id
            response = await client.post(f"{ASSISTANT_URL}/assistant/query", json=payload)
            response.raise_for_status()
            return response.json()

    async def get_session(self, session_id: str) -> dict:
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.get(f"{ASSISTANT_URL}/assistant/sessions/{session_id}")
            response.raise_for_status()
            return response.json()
