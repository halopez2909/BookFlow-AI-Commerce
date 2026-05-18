from datetime import datetime, timedelta
from typing import List, Optional
from collections import Counter
from sqlalchemy.orm import Session

from app.infrastructure.models import (
    AuditEventModel,
    PricingDecisionReadModel,
    EnrichmentRequestReadModel,
    EnrichmentResultReadModel,
    CartReadModel,
    CartItemReadModel,
    OrderReadModel,
    OrderItemReadModel,
    AssistantInteractionReadModel,
)
from app.domain.schemas import (
    AuditEventResponse,
    PricingHistoryItem,
    EnrichmentHistoryItem,
    BookSummaryResponse,
    OrderHistoryItem,
    OrderItemAudit,
    CartHistoryItem,
    CartItemAudit,
    AssistantInteractionItem,
    GlobalEventItem,
    GlobalSummaryResponse,
)
from app.domain.entities import EventType


# ──────────────────────────────────────────
# Casos de uso del Sprint 2 (sin cambios)
# ──────────────────────────────────────────

class GetPricingHistory:
    def __init__(self, pricing_db: Session):
        self.pricing_db = pricing_db

    def execute(self, book_reference: str) -> List[PricingHistoryItem]:
        rows = (
            self.pricing_db.query(PricingDecisionReadModel)
            .filter(PricingDecisionReadModel.book_reference == book_reference)
            .order_by(PricingDecisionReadModel.created_at.desc())
            .all()
        )
        return [
            PricingHistoryItem(
                id=row.id,
                book_reference=row.book_reference,
                suggested_price=row.suggested_price,
                explanation=row.explanation,
                condition_factor=row.condition_factor,
                source_used=None,
                timestamp=row.created_at or datetime.utcnow(),
            )
            for row in rows
        ]


class GetEnrichmentHistory:
    def __init__(self, enrichment_db: Session):
        self.enrichment_db = enrichment_db

    def execute(self, book_reference: str) -> List[EnrichmentHistoryItem]:
        requests = (
            self.enrichment_db.query(EnrichmentRequestReadModel)
            .filter(EnrichmentRequestReadModel.book_reference == book_reference)
            .order_by(EnrichmentRequestReadModel.requested_at.desc())
            .all()
        )
        result = []
        for req in requests:
            res = (
                self.enrichment_db.query(EnrichmentResultReadModel)
                .filter(EnrichmentResultReadModel.request_id == req.id)
                .first()
            )
            result.append(
                EnrichmentHistoryItem(
                    id=req.id,
                    book_reference=req.book_reference,
                    source_used=req.source_used,
                    status=req.status,
                    normalized_title=res.normalized_title if res else None,
                    normalized_author=res.normalized_author if res else None,
                    timestamp=req.requested_at or datetime.utcnow(),
                )
            )
        return result


class GetBookSummary:
    def __init__(self, pricing_db: Session, enrichment_db: Session):
        self.pricing_db = pricing_db
        self.enrichment_db = enrichment_db

    def execute(self, book_reference: str) -> BookSummaryResponse:
        pricing = GetPricingHistory(self.pricing_db).execute(book_reference)
        enrichment = GetEnrichmentHistory(self.enrichment_db).execute(book_reference)
        return BookSummaryResponse(
            book_reference=book_reference,
            pricing_history=pricing,
            enrichment_history=enrichment,
            total_pricing_decisions=len(pricing),
            total_enrichments=len(enrichment),
        )


class GetAuditEvents:
    def __init__(self, audit_db: Session):
        self.audit_db = audit_db

    def execute(self, from_date: Optional[datetime], to_date: Optional[datetime]) -> List[AuditEventResponse]:
        query = self.audit_db.query(AuditEventModel)
        if from_date:
            query = query.filter(AuditEventModel.timestamp >= from_date)
        if to_date:
            query = query.filter(AuditEventModel.timestamp <= to_date)
        rows = query.order_by(AuditEventModel.timestamp.desc()).all()
        return [
            AuditEventResponse(
                id=row.id,
                event_type=row.event_type,
                book_reference=row.book_reference,
                timestamp=row.timestamp,
                actor=row.actor,
                details=row.details,
            )
            for row in rows
        ]


# ──────────────────────────────────────────
# Casos de uso nuevos del Sprint 3
# ──────────────────────────────────────────

class GetOrderHistory:
    """
    Consulta el historial completo de pedidos de un cliente
    leyendo directamente desde order_db (solo lectura).
    """
    def __init__(self, order_db: Session):
        self.order_db = order_db

    def execute(self, customer_id: str) -> List[OrderHistoryItem]:
        orders = (
            self.order_db.query(OrderReadModel)
            .filter(OrderReadModel.customer_id == customer_id)
            .order_by(OrderReadModel.created_at.desc())
            .all()
        )
        result = []
        for order in orders:
            items_rows = (
                self.order_db.query(OrderItemReadModel)
                .filter(OrderItemReadModel.order_id == order.id)
                .all()
            )
            items = [
                OrderItemAudit(
                    book_id=item.book_id,
                    quantity=item.quantity or 0,
                    unit_price=item.unit_price or 0.0,
                )
                for item in items_rows
            ]
            result.append(
                OrderHistoryItem(
                    id=order.id,
                    customer_id=order.customer_id,
                    status=order.status or "unknown",
                    total_amount=order.total_amount,
                    created_at=order.created_at or datetime.utcnow(),
                    updated_at=order.updated_at,
                    items=items,
                )
            )
        return result


class GetCartHistory:
    """
    Consulta el historial de carritos de un cliente
    leyendo desde order_db (solo lectura).
    """
    def __init__(self, order_db: Session):
        self.order_db = order_db

    def execute(self, customer_id: str) -> List[CartHistoryItem]:
        carts = (
            self.order_db.query(CartReadModel)
            .filter(CartReadModel.customer_id == customer_id)
            .order_by(CartReadModel.created_at.desc())
            .all()
        )
        result = []
        for cart in carts:
            items_rows = (
                self.order_db.query(CartItemReadModel)
                .filter(CartItemReadModel.cart_id == cart.id)
                .all()
            )
            items = [
                CartItemAudit(
                    book_id=item.book_id,
                    quantity=item.quantity or 0,
                    unit_price=item.unit_price,
                )
                for item in items_rows
            ]
            result.append(
                CartHistoryItem(
                    id=cart.id,
                    customer_id=cart.customer_id,
                    status=cart.status or "unknown",
                    created_at=cart.created_at or datetime.utcnow(),
                    updated_at=cart.updated_at,
                    items=items,
                )
            )
        return result


class GetAssistantHistory:
    """
    Consulta el historial de conversaciones de una sesión con el asistente
    leyendo desde assistant_db (solo lectura).
    """
    def __init__(self, assistant_db: Session):
        self.assistant_db = assistant_db

    def execute(self, session_id: str) -> List[AssistantInteractionItem]:
        rows = (
            self.assistant_db.query(AssistantInteractionReadModel)
            .filter(AssistantInteractionReadModel.session_id == session_id)
            .order_by(AssistantInteractionReadModel.created_at.asc())
            .all()
        )
        return [
            AssistantInteractionItem(
                id=row.id,
                session_id=row.session_id,
                user_question=row.user_question or "",
                interpreted_intent=row.interpreted_intent,
                answer_text=row.answer_text,
                created_at=row.created_at or datetime.utcnow(),
            )
            for row in rows
        ]


class GetGlobalEvents:
    """
    Retorna todos los eventos del sistema filtrados por fecha y/o event_type.
    Lee de audit_db donde todos los servicios registran sus eventos.
    """
    def __init__(self, audit_db: Session):
        self.audit_db = audit_db

    def execute(
        self,
        from_date: Optional[datetime],
        to_date: Optional[datetime],
        event_type: Optional[EventType],
    ) -> List[GlobalEventItem]:
        query = self.audit_db.query(AuditEventModel)
        if from_date:
            query = query.filter(AuditEventModel.timestamp >= from_date)
        if to_date:
            query = query.filter(AuditEventModel.timestamp <= to_date)
        if event_type:
            query = query.filter(AuditEventModel.event_type == event_type.value)
        rows = query.order_by(AuditEventModel.timestamp.desc()).all()
        return [
            GlobalEventItem(
                id=row.id,
                event_type=row.event_type,
                book_reference=row.book_reference,
                timestamp=row.timestamp,
                actor=row.actor,
                details=row.details,
            )
            for row in rows
        ]


class GetGlobalSummary:
    """
    Calcula métricas del sistema sobre los últimos `days` días:
    - total_orders, total_carts
    - cart_to_order_rate: % de carritos que terminaron en pedido
    - top_books: libros más consultados (por audit_events de tipo cart_add + assistant_query)
    - top_assistant_intents: intenciones más frecuentes del asistente
    - orders_by_status: distribución de pedidos por estado
    """
    def __init__(self, audit_db: Session, order_db: Session, assistant_db: Session):
        self.audit_db = audit_db
        self.order_db = order_db
        self.assistant_db = assistant_db

    def execute(self, days: int = 7) -> GlobalSummaryResponse:
        since = datetime.utcnow() - timedelta(days=days)

        # Total pedidos en el período
        total_orders = (
            self.order_db.query(OrderReadModel)
            .filter(OrderReadModel.created_at >= since)
            .count()
        )

        # Total carritos en el período
        total_carts = (
            self.order_db.query(CartReadModel)
            .filter(CartReadModel.created_at >= since)
            .count()
        )

        # Tasa de conversión carrito → pedido
        cart_to_order_rate = (
            round(total_orders / total_carts * 100, 2) if total_carts > 0 else 0.0
        )

        # Top books: book_reference más frecuentes en eventos cart_add del período
        cart_add_events = (
            self.audit_db.query(AuditEventModel)
            .filter(
                AuditEventModel.event_type == EventType.CART_ADD.value,
                AuditEventModel.timestamp >= since,
            )
            .all()
        )
        book_counter = Counter(e.book_reference for e in cart_add_events)
        top_books = [book for book, _ in book_counter.most_common(5)]

        # Top intenciones del asistente
        interactions = (
            self.assistant_db.query(AssistantInteractionReadModel)
            .filter(AssistantInteractionReadModel.created_at >= since)
            .all()
        )
        intent_counter = Counter(
            i.interpreted_intent for i in interactions if i.interpreted_intent
        )
        top_intents = [intent for intent, _ in intent_counter.most_common(5)]

        # Distribución de pedidos por estado
        all_orders = (
            self.order_db.query(OrderReadModel)
            .filter(OrderReadModel.created_at >= since)
            .all()
        )
        status_counter = Counter(o.status for o in all_orders if o.status)
        orders_by_status = dict(status_counter)

        return GlobalSummaryResponse(
            period_days=days,
            total_orders=total_orders,
            total_carts=total_carts,
            cart_to_order_rate=cart_to_order_rate,
            top_books=top_books,
            top_assistant_intents=top_intents,
            orders_by_status=orders_by_status,
        )
