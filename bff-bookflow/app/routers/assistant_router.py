"""Assistant router (Sprint 3 - Dev 6 Jenn).
Gateway hacia ai-assistant-service. Rutas PUBLICAS (sin JWT).
"""
from fastapi import APIRouter, HTTPException, Request
from app.infrastructure.clients.assistant_client import AssistantClient
from app.routers.cart_router import limiter

router = APIRouter(prefix="/api/assistant", tags=["assistant"])


@router.post("/query")
@limiter.limit("100/minute")
async def assistant_query(request: Request, payload: dict):
    """Consulta libre al asistente IA. Publico."""
    query_text = payload.get("query")
    if not query_text:
        raise HTTPException(status_code=400, detail="query es obligatorio")
    session_id = payload.get("session_id")
    customer_id = payload.get("customer_id")
    try:
        client = AssistantClient()
        return await client.query(query_text, session_id=session_id, customer_id=customer_id)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"assistant-service unavailable: {e}")


@router.get("/sessions/{session_id}")
@limiter.limit("100/minute")
async def get_session(request: Request, session_id: str):
    """Recupera el historial de una sesion del asistente."""
    try:
        client = AssistantClient()
        return await client.get_session(session_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"session not found: {e}")
