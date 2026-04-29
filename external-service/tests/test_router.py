import pytest
from app.routers.external_router import router


def test_router_has_lookup_route():
    routes = [r.path for r in router.routes]
    assert "/external/lookup" in routes


def test_router_has_health_route():
    routes = [r.path for r in router.routes]
    assert "/external/health" in routes


def test_router_prefix():
    assert router.prefix == "/external"
