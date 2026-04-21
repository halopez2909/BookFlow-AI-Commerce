import pytest
import asyncio
from app.infrastructure.providers.mock_provider import MockEnrichmentProvider


def test_mock_provider_returns_result():
    provider = MockEnrichmentProvider()
    result = asyncio.run(provider.enrich(
        book_reference="REF001",
        title="Test Book",
        author="Test Author",
        isbn="9781234567890",
    ))
    assert result is not None
    assert result.normalized_title is not None
    assert "[MOCK]" in result.normalized_title


def test_mock_provider_uses_provided_title():
    provider = MockEnrichmentProvider()
    result = asyncio.run(provider.enrich(
        book_reference="REF001",
        title="My Book",
        author="Author",
        isbn="",
    ))
    assert "My Book" in result.normalized_title
