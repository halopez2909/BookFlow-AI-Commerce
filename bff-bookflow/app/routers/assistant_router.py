from fastapi import APIRouter, HTTPException
import httpx
import os

router = APIRouter(prefix="/api/assistant", tags=["assistant"])
ASSISTANT_URL = os.getenv("ASSISTANT_URL", "http://ai-assistant-service:8012")

@router.post("/query")
async def query_assistant(data: dict):
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.post(f"{ASSISTANT_URL}/assistant/query", json=data)
            r.raise_for_status()
            return r.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sessions/{session_id}")
async def get_session(session_id: str):
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(f"{ASSISTANT_URL}/assistant/sessions/{session_id}")
            r.raise_for_status()
            return r.json()
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
