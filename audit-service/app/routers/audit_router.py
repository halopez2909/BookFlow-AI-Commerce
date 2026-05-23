from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.application.use_cases import (
    # Sprint 2
    GetPricingHistory,
    GetEnrichmentHistory,
    GetBookSummary,
    GetAuditEvents,
    # Sprint 3
    GetOrderHistory,
    GetCartHistory,
    GetAssistantHistory,
    GetGlobalEvents,
    GetGlobalSummary,
)
from app.domain.schemas import (
    # Sprint 2
    AuditEventResponse,
    PricingHistoryItem,
    EnrichmentHistoryItem,
    BookSummaryResponse,
    # Sprint 3
    OrderHistoryItem,
    CartHistoryItem,
    AssistantInteractionItem,
    GlobalEventItem,
    GlobalSummaryResponse,
)
from app.domain.entities import EventType
from app.infrastructure.database import (
    get_audit_db,
    get_pricing_db,
    get_enrichment_db,
    get_order_db,
    get_assistant_db,
)

router = APIRouter(prefix="/audit", tags=["audit"])


# ──────────────────────────────────────────
# Endpoints Sprint 2 (sin cambios)
# ──────────────────────────────────────────

@router.get("/pricing/{book_reference}", response_model=List[PricingHistoryItem])
def get_pricing_history(
    book_reference: str,
    pricing_db: Session = Depends(get_pricing_db),
):
    try:
        return GetPricingHistory(pricing_db).execute(book_reference)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/enrichment/{book_reference}", response_model=List[EnrichmentHistoryItem])
def get_enrichment_history(
    book_reference: str,
    enrichment_db: Session = Depends(get_enrichment_db),
):
    try:
        return GetEnrichmentHistory(enrichment_db).execute(book_reference)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/summary/{book_reference}", response_model=BookSummaryResponse)
def get_book_summary(
    book_reference: str,
    pricing_db: Session = Depends(get_pricing_db),
    enrichment_db: Session = Depends(get_enrichment_db),
):
    try:
        return GetBookSummary(pricing_db, enrichment_db).execute(book_reference)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/events", response_model=List[AuditEventResponse])
def get_audit_events(
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None,
    audit_db: Session = Depends(get_audit_db),
):
    try:
        return GetAuditEvents(audit_db).execute(from_date, to_date)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# ──────────────────────────────────────────
# Endpoints nuevos Sprint 3
# ──────────────────────────────────────────

@router.get("/orders/{customer_id}", response_model=List[OrderHistoryItem])
def get_order_history(
    customer_id: str,
    order_db: Session = Depends(get_order_db),
):
    """
    Historial completo de pedidos de un cliente con estados, ítems y precios.
    Solo lectura desde order_db.
    """
    try:
        return GetOrderHistory(order_db).execute(customer_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/cart/{customer_id}", response_model=List[CartHistoryItem])
def get_cart_history(
    customer_id: str,
    order_db: Session = Depends(get_order_db),
):
    """
    Historial de carritos del cliente, incluyendo ítems agregados.
    Solo lectura desde order_db.
    """
    try:
        return GetCartHistory(order_db).execute(customer_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/assistant/{session_id}", response_model=List[AssistantInteractionItem])
def get_assistant_history(
    session_id: str,
    assistant_db: Session = Depends(get_assistant_db),
):
    """
    Historial de conversaciones de una sesión con el asistente IA.
    Solo lectura desde assistant_db.
    """
    try:
        return GetAssistantHistory(assistant_db).execute(session_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/global/events", response_model=List[GlobalEventItem])
def get_global_events(
    from_date: Optional[datetime] = Query(None, description="Fecha inicio (ISO 8601)"),
    to_date: Optional[datetime] = Query(None, description="Fecha fin (ISO 8601)"),
    event_type: Optional[EventType] = Query(None, description="Tipo de evento a filtrar"),
    audit_db: Session = Depends(get_audit_db),
):
    """
    Todos los eventos del sistema en un rango de fechas, filtrables por tipo.
    Tipos disponibles: cart_add, cart_remove, order_created, order_confirmed,
    order_cancelled, assistant_query, recommendation_viewed,
    pricing_decision, enrichment_completed, normalization_applied.
    """
    try:
        return GetGlobalEvents(audit_db).execute(from_date, to_date, event_type)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/global/summary", response_model=GlobalSummaryResponse)
def get_global_summary(
    days: int = Query(7, ge=1, le=90, description="Período en días (por defecto 7)"),
    audit_db: Session = Depends(get_audit_db),
    order_db: Session = Depends(get_order_db),
    assistant_db: Session = Depends(get_assistant_db),
):
    """
    Métricas del sistema para los últimos N días:
    total de pedidos, tasa de conversión carrito→pedido,
    libros más consultados e intenciones más frecuentes del asistente.
    """
    try:
        return GetGlobalSummary(audit_db, order_db, assistant_db).execute(days)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
