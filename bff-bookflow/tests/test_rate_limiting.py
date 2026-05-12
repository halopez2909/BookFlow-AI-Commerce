"""Sprint 3 - Dev 6 Jenn.
Test del Throttling Pattern (slowapi):
    - Rutas publicas: 100 req/min por IP
    - Rutas autenticadas: 300 req/min por IP
"""
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from slowapi.errors import RateLimitExceeded

import main as main_module
from main import app


def _reset_limiter():
    """Reinicia el storage del rate limiter entre tests."""
    main_module.global_limiter.reset()


def test_public_route_rate_limit_429():
    """Hacer >100 requests publicos en una ventana debe terminar en 429."""
    _reset_limiter()
    rec_mock = AsyncMock(return_value={"items": []})
    with patch(
        "app.infrastructure.clients.recommender_client.RecommenderClient.get_popular",
        rec_mock,
    ):
        client = TestClient(app)
        statuses = []
        for _ in range(105):
            r = client.get("/api/recommendations/popular")
            statuses.append(r.status_code)
        # debe haber al menos un 429 en la rafaga
        assert 429 in statuses, f"Esperaba 429 al superar 100/min, vi: {set(statuses)}"


def test_unauth_health_no_rate_limit_strict():
    """El health basico /health (no /api/health) no usa limiter, debe responder 200 siempre."""
    _reset_limiter()
    client = TestClient(app)
    for _ in range(20):
        r = client.get("/health")
        assert r.status_code == 200
        assert r.json()["service"] == "bff-bookflow"
