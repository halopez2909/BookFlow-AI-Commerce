import pytest
from app.routers.integration_router import router


def test_router_has_trigger_route():
    routes = [r.path for r in router.routes]
    assert "/integration/trigger/{batch_id}" in routes


def test_router_has_status_route():
    routes = [r.path for r in router.routes]
    assert "/integration/status/{batch_id}" in routes


def test_router_has_flows_route():
    routes = [r.path for r in router.routes]
    assert "/integration/flows" in routes


def test_router_has_health_route():
    routes = [r.path for r in router.routes]
    assert "/integration/health" in routes
