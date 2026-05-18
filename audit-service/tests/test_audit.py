import uuid
from datetime import datetime
from unittest.mock import MagicMock
from app.application.use_cases import GetPricingHistory, GetEnrichmentHistory, GetBookSummary, GetAuditEvents
from app.infrastructure.models import PricingDecisionReadModel, EnrichmentRequestReadModel, AuditEventModel


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


def test_get_pricing_history_returns_list():
    db = MagicMock()
    db.query.return_value.filter.return_value.order_by.return_value.all.return_value = [make_pricing_row()]

    use_case = GetPricingHistory(db)
    result = use_case.execute("book-001")

    assert len(result) == 1
    assert result[0].book_reference == "book-001"
    assert result[0].suggested_price == 25000.0


def test_get_pricing_history_empty():
    db = MagicMock()
    db.query.return_value.filter.return_value.order_by.return_value.all.return_value = []

    use_case = GetPricingHistory(db)
    result = use_case.execute("libro-no-existe")

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

    use_case = GetBookSummary(pricing_db, enrichment_db)
    summary = use_case.execute("book-001")

    assert summary.book_reference == "book-001"
    assert summary.total_pricing_decisions == 2
    assert summary.total_enrichments == 1


def test_get_audit_events_date_filter():
    db = MagicMock()
    db.query.return_value.filter.return_value.filter.return_value.order_by.return_value.all.return_value = []

    use_case = GetAuditEvents(db)
    result = use_case.execute(from_date=datetime(2024, 1, 1), to_date=datetime(2024, 12, 31))
    assert result == []
