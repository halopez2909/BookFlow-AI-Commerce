from fastapi import APIRouter, HTTPException
from typing import Optional
import httpx
import os

router = APIRouter(prefix="/api/recommendations", tags=["recommendations"])
RECOMMENDER_URL = os.getenv("RECOMMENDER_URL", "http://recommender-service:8090")

@router.get("/popular")
async def get_popular():
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(f"{RECOMMENDER_URL}/recommendations/popular")
            r.raise_for_status()
            return r.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{book_id}")
async def get_recommendations(book_id: str, strategy: Optional[str] = None):
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            params = {"strategy": strategy} if strategy else {}
            r = await client.get(f"{RECOMMENDER_URL}/recommendations/{book_id}", params=params)
            r.raise_for_status()
            return r.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
