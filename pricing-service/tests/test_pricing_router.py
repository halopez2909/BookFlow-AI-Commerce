import pytest
from app.routers.pricing_router import router


def test_router_has_calculate_route():
    routes = [r.path for r in router.routes]
    assert "/pricing/calculate" in routes


def test_router_has_decisions_route():
    routes = [r.path for r in router.routes]
    assert "/pricing/decisions/{book_reference}" in routes


def test_router_has_all_decisions_route():
    routes = [r.path for r in router.routes]
    assert "/pricing/decisions" in routes


def test_router_has_health_route():
    routes = [r.path for r in router.routes]
    assert "/pricing/health" in routes
