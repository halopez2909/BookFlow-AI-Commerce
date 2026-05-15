"""
Router HTTP del AI Assistant Service. Expone:
  - POST /assistant/query                       -> procesa una pregunta.
  - GET  /assistant/sessions/{session_id}       -> devuelve el historial.

La construcción del ProcessQuery se hace en factories anotadas con
Depends, lo que permite testear el router con overrides en pytest.
"""
from functools import lru_cache

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.application.use_cases import GetSessionHistory, ProcessQuery
from app.domain.intent_classifier import IntentClassifier
from app.domain.repositories import AssistantInteractionRepository
from app.domain.response_builder import ResponseBuilder
from app.domain.schemas import (
    InteractionOut,
    QueryRequest,
    QueryResponse,
    SessionHistoryResponse,
)
from app.infrastructure.clients.catalog_client import CatalogClient
from app.infrastructure.clients.inventory_client import InventoryClient
from app.infrastructure.clients.pricing_client import PricingClient
from app.infrastructure.database import get_db
from app.infrastructure.providers.fallback_classifier import FallbackClassifier
from app.infrastructure.providers.intent_classifier import AIClassifier
from app.infrastructure.repositories import AssistantInteractionRepositoryPostgres

router = APIRouter(prefix="/assistant", tags=["assistant"])


# -------------- Dependency factories --------------
# Reutilizables como singletons (no tienen estado mutable).

@lru_cache(maxsize=1)
def get_ai_classifier() -> IntentClassifier:
    return AIClassifier()


@lru_cache(maxsize=1)
def get_fallback_classifier() -> IntentClassifier:
    return FallbackClassifier()


@lru_cache(maxsize=1)
def get_catalog_client() -> CatalogClient:
    return CatalogClient()


@lru_cache(maxsize=1)
def get_inventory_client() -> InventoryClient:
    return InventoryClient()


@lru_cache(maxsize=1)
def get_pricing_client() -> PricingClient:
    return PricingClient()


@lru_cache(maxsize=1)
def get_response_builder() -> ResponseBuilder:
    return ResponseBuilder()


# Por request (depende de la Session de SQLAlchemy)
def get_repository(db: Session = Depends(get_db)) -> AssistantInteractionRepository:
    return AssistantInteractionRepositoryPostgres(db)


def get_process_query_use_case(
    ai_classifier: IntentClassifier = Depends(get_ai_classifier),
    fallback_classifier: IntentClassifier = Depends(get_fallback_classifier),
    catalog_client: CatalogClient = Depends(get_catalog_client),
    inventory_client: InventoryClient = Depends(get_inventory_client),
    pricing_client: PricingClient = Depends(get_pricing_client),
    response_builder: ResponseBuilder = Depends(get_response_builder),
    repository: AssistantInteractionRepository = Depends(get_repository),
) -> ProcessQuery:
    return ProcessQuery(
        ai_classifier=ai_classifier,
        fallback_classifier=fallback_classifier,
        catalog_client=catalog_client,
        inventory_client=inventory_client,
        pricing_client=pricing_client,
        response_builder=response_builder,
        repository=repository,
    )


def get_history_use_case(
    repository: AssistantInteractionRepository = Depends(get_repository),
) -> GetSessionHistory:
    return GetSessionHistory(repository)


# -------------- Endpoints --------------

@router.post(
    "/query",
    response_model=QueryResponse,
    status_code=status.HTTP_200_OK,
    summary="Procesa una pregunta del usuario y devuelve la respuesta del asistente.",
)
async def post_query(
    payload: QueryRequest,
    use_case: ProcessQuery = Depends(get_process_query_use_case),
) -> QueryResponse:
    try:
        result = await use_case.execute(
            session_id=payload.session_id,
            question=payload.question,
        )
    except Exception as exc:  # noqa: BLE001 -- frontera HTTP, no propagamos stack
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"No se pudo procesar la consulta: {exc}",
        ) from exc
    return QueryResponse(
        answer=result["answer"],
        intent=result["intent"],
        sources=result["sources"],
    )


@router.get(
    "/sessions/{session_id}",
    response_model=SessionHistoryResponse,
    summary="Devuelve el historial de preguntas y respuestas de una sesión.",
)
def get_session_history(
    session_id: str,
    use_case: GetSessionHistory = Depends(get_history_use_case),
) -> SessionHistoryResponse:
    interactions = use_case.execute(session_id)
    return SessionHistoryResponse(
        session_id=session_id,
        interactions=[
            InteractionOut(
                id=i.id,
                session_id=i.session_id,
                user_question=i.user_question,
                interpreted_intent=i.interpreted_intent,
                answer_text=i.answer_text,
                created_at=i.created_at,
            )
            for i in interactions
        ],
    )