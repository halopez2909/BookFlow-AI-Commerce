# bff-bookflow/app/routers/recommendations_router.py
from fastapi import APIRouter, Query, HTTPException
import httpx
import os

router = APIRouter(prefix="/recommendations", tags=["BFF Recommendations"])
RECOMMENDER_URL = os.getenv("RECOMMENDER_SERVICE_URL", "http://localhost:8090")

@router.get("/popular")
def get_popular():
    with httpx.Client() as client:
        response = client.get(f"{RECOMMENDER_URL}/recommendations/popular")
        return response.json()

@router.get("/{book_id}")
def get_recommendations(book_id: str, strategy: str = Query(None)):
    with httpx.Client() as client:
        params = {"strategy": strategy} if strategy else {}
        response = client.get(f"{RECOMMENDER_URL}/recommendations/{book_id}", params=params)
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Recommendations not found")
        return response.json()