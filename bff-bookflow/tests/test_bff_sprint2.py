import pytest
from unittest.mock import AsyncMock, patch, MagicMock


def test_normalization_router_routes():
    from app.routers.normalization_router import router
    routes = [r.path for r in router.routes]
    assert '/api/normalization/normalize' in routes
    assert '/api/normalization/batch' in routes
    assert '/api/normalization/records' in routes


def test_pricing_router_routes():
    from app.routers.pricing_router import router
    routes = [r.path for r in router.routes]
    assert '/api/pricing/calculate' in routes
    assert '/api/pricing/decisions/{book_reference}' in routes


def test_audit_router_routes():
    from app.routers.audit_router import router
    routes = [r.path for r in router.routes]
    assert '/api/audit/summary/{book_reference}' in routes
    assert '/api/audit/pricing/{book_reference}' in routes
    assert '/api/audit/enrichment/{book_reference}' in routes


def test_integration_router_routes():
    from app.routers.integration_router import router
    routes = [r.path for r in router.routes]
    assert '/api/integration/trigger/{batch_id}' in routes


def test_system_router_routes():
    from app.routers.system_router import router
    routes = [r.path for r in router.routes]
    assert '/api/system/health' in routes


def test_normalization_client_exists():
    from app.infrastructure.clients.normalization_client import NormalizationClient
    client = NormalizationClient()
    assert hasattr(client, 'normalize')
    assert hasattr(client, 'normalize_batch')
    assert hasattr(client, 'get_records')


def test_pricing_client_exists():
    from app.infrastructure.clients.pricing_client import PricingClient
    client = PricingClient()
    assert hasattr(client, 'calculate')
    assert hasattr(client, 'get_decision')


def test_audit_client_exists():
    from app.infrastructure.clients.audit_client import AuditClient
    client = AuditClient()
    assert hasattr(client, 'get_summary')
    assert hasattr(client, 'get_pricing_audit')
    assert hasattr(client, 'get_enrichment_audit')


def test_integration_client_exists():
    from app.infrastructure.clients.integration_client import IntegrationClient
    client = IntegrationClient()
    assert hasattr(client, 'trigger')
    assert hasattr(client, 'external_health')
