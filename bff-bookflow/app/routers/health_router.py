"""Health router publico (Sprint 3).
Atajo /api/health -> mismo health agregado del system_router.
"""
from fastapi import APIRouter
from app.routers.system_router import system_health

router = APIRouter(prefix="/api", tags=["health"])


@router.get("/health")
async def api_health():
    return await system_health()
