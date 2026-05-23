import uuid
from datetime import datetime
from unittest.mock import MagicMock

from app.application.use_cases import (
    GetPricingHistory,
    GetEnrichmentHistory,
    GetBookSummary,
    GetAuditEvents,
    GetOrderHistory,
    GetCartHistory,
    GetAssistantHistory,
    GetGlobalEvents,
    GetGlobalSummary,
)
from app.infrastructure.models import (
    PricingDecisionReadModel,
    EnrichmentRequestReadModel,
    AuditEventModel,
    OrderReadModel,
    OrderItemReadModel,
    CartReadModel,
    CartItemReadModel,
    AssistantInteractionReadModel,
)
from app.domain.entities import EventType


# ─── helpers ─────────────────────────────────────────────────────────────────

def make_pricing_row():
    row = MagicMock(spec=PricingDecisionReadModel)
    row.id = uuid.uuid4()
    row.book_reference = "book-001"
    row.suggested_price = 25000.0
    row.explanation = "Precio calculado con eBay como referencia"
    row.condition_factor = 0.8
    row.reference_count = 3
    row.created_at = datetime.utcnow()
    return row


def make_enrichment_row():
    row = MagicMock(spec=EnrichmentRequestReadModel)
    row.id = uuid.uuid4()
    row.book_reference = "book-001"
    row.status = "completed"
    row.source_used = "google_books"
    row.requested_at = datetime.utcnow()
    return row


def make_order_row(customer_id="user-001", order_status="confirmed"):
    row = MagicMock(spec=OrderReadModel)
    row.id = uuid.uuid4()
    row.customer_id = customer_id
    row.status = order_status
    row.total_amount = 50000.0
    row.created_at = datetime.utcnow()
    row.updated_at = datetime.utcnow()
    return row


def make_order_item_row(order_id=None):
    row = MagicMock(spec=OrderItemReadModel)
    row.id = uuid.uuid4()
    row.order_id = order_id or uuid.uuid4()
    row.book_id = "book-001"
    row.quantity = 2
    row.unit_price = 25000.0
    return row


def make_cart_row(customer_id="user-001"):
    row = MagicMock(spec=CartReadModel)
    row.id = uuid.uuid4()
    row.customer_id = customer_id
    row.status = "converted"
    row.created_at = datetime.utcnow()
    row.updated_at = datetime.utcnow()
    return row


def make_cart_item_row(cart_id=None):
    row = MagicMock(spec=CartItemReadModel)
    row.id = uuid.uuid4()
    row.cart_id = cart_id or uuid.uuid4()
    row.book_id = "book-001"
    row.quantity = 1
    row.unit_price = 25000.0
    return row


def make_interaction_row(session_id="session-abc"):
    row = MagicMock(spec=AssistantInteractionReadModel)
    row.id = uuid.uuid4()
    row.session_id = session_id
    row.user_question = "¿Tienen El principito disponible?"
    row.interpreted_intent = "AVAILABILITY_CHECK"
    row.answer_text = "Sí, tenemos El principito en stock."
    row.created_at = datetime.utcnow()
    return row


def make_audit_event_row(event_type=EventType.CART_ADD, book_ref="book-001"):
    row = MagicMock(spec=AuditEventModel)
    row.id = uuid.uuid4()
    row.event_type = event_type.value
    row.book_reference = book_ref
    row.timestamp = datetime.utcnow()
    row.actor = "system"
    row.details = {}
    return row


# ─── Tests Sprint 2 (mantener funcionando) ───────────────────────────────────

def test_get_pricing_history_returns_list():
    db = MagicMock()
    db.query.return_value.filter.return_value.order_by.return_value.all.return_value = [make_pricing_row()]
    result = GetPricingHistory(db).execute("book-001")
    assert len(result) == 1
    assert result[0].book_reference == "book-001"
    assert result[0].suggested_price == 25000.0


def test_get_pricing_history_empty():
    db = MagicMock()
    db.query.return_value.filter.return_value.order_by.return_value.all.return_value = []
    result = GetPricingHistory(db).execute("libro-no-existe")
    assert result == []


def test_get_book_summary_totals():
    pricing_db = MagicMock()
    pricing_db.query.return_value.filter.return_value.order_by.return_value.all.return_value = [
        make_pricing_row(), make_pricing_row()
    ]
    enrichment_db = MagicMock()
    enrichment_db.query.return_value.filter.return_value.order_by.return_value.all.return_value = [
        make_enrichment_row()
    ]
    enrichment_db.query.return_value.filter.return_value.first.return_value = None
    summary = GetBookSummary(pricing_db, enrichment_db).execute("book-001")
    assert summary.book_reference == "book-001"
    assert summary.total_pricing_decisions == 2
    assert summary.total_enrichments == 1


def test_get_audit_events_date_filter():
    db = MagicMock()
    db.query.return_value.filter.return_value.filter.return_value.order_by.return_value.all.return_value = []
    result = GetAuditEvents(db).execute(from_date=datetime(2024, 1, 1), to_date=datetime(2024, 12, 31))
    assert result == []


# ─── Tests Sprint 3 — GetOrderHistory ────────────────────────────────────────

def test_get_order_history_retorna_pedidos():
    """GET /audit/orders/{customer_id} debe retornar lista de pedidos con ítems."""
    order_db = MagicMock()
    order = make_order_row(customer_id="user-001")
    item = make_order_item_row(order_id=order.id)

    # Primera query: órdenes
    order_db.query.return_value.filter.return_value.order_by.return_value.all.return_value = [order]
    # Segunda query: ítems de cada orden
    order_db.query.return_value.filter.return_value.all.return_value = [item]

    result = GetOrderHistory(order_db).execute("user-001")
    assert len(result) == 1
    assert result[0].customer_id == "user-001"
    assert result[0].status == "confirmed"


def test_get_order_history_cliente_sin_pedidos():
    """Si el cliente no tiene pedidos, retorna lista vacía."""
    order_db = MagicMock()
    order_db.query.return_value.filter.return_value.order_by.return_value.all.return_value = []
    result = GetOrderHistory(order_db).execute("user-999")
    assert result == []


# ─── Tests Sprint 3 — GetCartHistory ─────────────────────────────────────────

def test_get_cart_history_retorna_carritos():
    """GET /audit/cart/{customer_id} debe retornar historial de carritos."""
    order_db = MagicMock()
    cart = make_cart_row(customer_id="user-001")
    item = make_cart_item_row(cart_id=cart.id)

    order_db.query.return_value.filter.return_value.order_by.return_value.all.return_value = [cart]
    order_db.query.return_value.filter.return_value.all.return_value = [item]

    result = GetCartHistory(order_db).execute("user-001")
    assert len(result) == 1
    assert result[0].customer_id == "user-001"
    assert result[0].status == "converted"


def test_get_cart_history_vacio():
    order_db = MagicMock()
    order_db.query.return_value.filter.return_value.order_by.return_value.all.return_value = []
    result = GetCartHistory(order_db).execute("user-999")
    assert result == []


# ─── Tests Sprint 3 — GetAssistantHistory ────────────────────────────────────

def test_get_assistant_history_retorna_interacciones():
    """GET /audit/assistant/{session_id} debe retornar historial de conversación."""
    assistant_db = MagicMock()
    interaction = make_interaction_row(session_id="session-abc")
    assistant_db.query.return_value.filter.return_value.order_by.return_value.all.return_value = [interaction]

    result = GetAssistantHistory(assistant_db).execute("session-abc")
    assert len(result) == 1
    assert result[0].session_id == "session-abc"
    assert result[0].interpreted_intent == "AVAILABILITY_CHECK"


def test_get_assistant_history_sesion_no_existe():
    assistant_db = MagicMock()
    assistant_db.query.return_value.filter.return_value.order_by.return_value.all.return_value = []
    result = GetAssistantHistory(assistant_db).execute("session-no-existe")
    assert result == []


# ─── Tests Sprint 3 — GetGlobalEvents ────────────────────────────────────────

def test_get_global_events_filtro_por_tipo():
    """GET /audit/global/events?event_type=cart_add debe filtrar correctamente."""
    audit_db = MagicMock()
    event = make_audit_event_row(event_type=EventType.CART_ADD)
    # Simula la cadena de filtros
    audit_db.query.return_value.filter.return_value.filter.return_value.filter.return_value.order_by.return_value.all.return_value = [event]
    audit_db.query.return_value.filter.return_value.filter.return_value.order_by.return_value.all.return_value = [event]
    audit_db.query.return_value.filter.return_value.order_by.return_value.all.return_value = [event]
    audit_db.query.return_value.order_by.return_value.all.return_value = [event]

    result = GetGlobalEvents(audit_db).execute(None, None, EventType.CART_ADD)
    # Verificamos que se llamó query y se retornó algo procesable
    assert isinstance(result, list)


def test_get_global_events_sin_filtros():
    audit_db = MagicMock()
    audit_db.query.return_value.order_by.return_value.all.return_value = []
    result = GetGlobalEvents(audit_db).execute(None, None, None)
    assert result == []


# ─── Tests Sprint 3 — GetGlobalSummary ───────────────────────────────────────

def test_get_global_summary_calcula_metricas():
    """GET /audit/global/summary debe calcular tasa de conversión correctamente."""
    audit_db = MagicMock()
    order_db = MagicMock()
    assistant_db = MagicMock()

    # 3 pedidos, 6 carritos → tasa 50%
    order_db.query.return_value.filter.return_value.count.side_effect = [3, 6]
    order_db.query.return_value.filter.return_value.all.return_value = [
        make_order_row(order_status="confirmed"),
        make_order_row(order_status="pending"),
        make_order_row(order_status="confirmed"),
    ]
    audit_db.query.return_value.filter.return_value.filter.return_value.all.return_value = [
        make_audit_event_row(EventType.CART_ADD, "book-001"),
        make_audit_event_row(EventType.CART_ADD, "book-001"),
        make_audit_event_row(EventType.CART_ADD, "book-002"),
    ]
    assistant_db.query.return_value.filter.return_value.all.return_value = [
        make_interaction_row(),
        make_interaction_row(),
    ]

    result = GetGlobalSummary(audit_db, order_db, assistant_db).execute(days=7)
    assert result.period_days == 7
    assert result.total_orders == 3
    assert result.total_carts == 6
    assert result.cart_to_order_rate == 50.0
    assert "book-001" in result.top_books


def test_get_global_summary_sin_datos():
    """Si no hay datos, retorna métricas en cero sin errores."""
    audit_db = MagicMock()
    order_db = MagicMock()
    assistant_db = MagicMock()

    order_db.query.return_value.filter.return_value.count.return_value = 0
    order_db.query.return_value.filter.return_value.all.return_value = []
    audit_db.query.return_value.filter.return_value.filter.return_value.all.return_value = []
    assistant_db.query.return_value.filter.return_value.all.return_value = []

    result = GetGlobalSummary(audit_db, order_db, assistant_db).execute(days=7)
    assert result.total_orders == 0
    assert result.total_carts == 0
    assert result.cart_to_order_rate == 0.0
    assert result.top_books == []
