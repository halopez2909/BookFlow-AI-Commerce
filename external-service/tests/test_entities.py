import pytest
from app.domain.entities import ExternalApiResult, ApiHealthStatus
from datetime import datetime


def test_external_api_result_ok():
    result = ExternalApiResult.ok("google_books", {"title": "Clean Code"}, 150.0)
    assert result.success is True
    assert result.source == "google_books"
    assert result.data["title"] == "Clean Code"
    assert result.latency_ms == 150.0
    assert result.cached is False


def test_external_api_result_fail():
    result = ExternalApiResult.fail("google_books", "Timeout", 5000.0)
    assert result.success is False
    assert result.error == "Timeout"
    assert result.data is None


def test_external_api_result_cached():
    result = ExternalApiResult.ok("open_library", {"title": "1984"}, 0, cached=True)
    assert result.cached is True
    assert result.latency_ms == 0


def test_api_health_status():
    status = ApiHealthStatus(
        name="google_books", status="ok",
        latency_ms=120.0, last_checked=datetime.utcnow()
    )
    assert status.name == "google_books"
    assert status.status == "ok"
    assert status.error is None
