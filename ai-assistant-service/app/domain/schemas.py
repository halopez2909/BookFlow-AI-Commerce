"""
Schemas Pydantic v2 para los contratos HTTP del asistente.
Son los DTOs que FastAPI usa para validar request/response.
"""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from app.domain.intents import IntentType


# ---------- Request ----------

class QueryRequest(BaseModel):
    session_id: str = Field(..., min_length=1, max_length=128,
                            description="Identificador único de la sesión del usuario.")
    question: str = Field(..., min_length=1, max_length=500,
                          description="Pregunta del usuario en lenguaje natural.")


# ---------- Response ----------

class QueryResponse(BaseModel):
    answer: str
    intent: IntentType
    sources: List[str] = Field(
        default_factory=list,
        description="Servicios consultados para construir la respuesta "
                    "(catalog, inventory, pricing).",
    )


class InteractionOut(BaseModel):
    id: str
    session_id: str
    user_question: str
    interpreted_intent: IntentType
    answer_text: str
    created_at: datetime


class SessionHistoryResponse(BaseModel):
    session_id: str
    interactions: List[InteractionOut]