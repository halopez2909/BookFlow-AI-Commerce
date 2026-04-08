import pytest
import asyncio
import uuid
from unittest.mock import MagicMock, AsyncMock
from app.application.use_cases import EnrichBook
from app.domain.schemas import EnrichBookRequest
from app.domain.entities import EnrichmentResult


def test_enrich_book_success():
    mock_provider = MagicMock()
    mock_result = EnrichmentResult(
        id=uuid.uuid4(),
        request_id=uuid.uuid4(),
        normalized_title="Test Book",
        normalized_author="Test Author",
        normalized_publisher="Test Publisher",
        normalized_description="Test Description",
        cover_url="http://example.com/cover.jpg",
        metadata_json={},
    )
    mock_provider.enrich = AsyncMock(return_value=mock_result)

    mock_request_repo = MagicMock()
    mock_request_repo.save = MagicMock(return_value=MagicMock(id=uuid.uuid4()))
    mock_request_repo.update_status = MagicMock()

    mock_result_repo = MagicMock()
    mock_result_repo.save = MagicMock(return_value=mock_result)

    use_case = EnrichBook(
        provider=mock_provider,
        request_repo=mock_request_repo,
        result_repo=mock_result_repo,
    )

    request = EnrichBookRequest(
        book_reference="REF001",
        title="Test Book",
        author="Test Author",
        isbn="9781234567890",
    )

    result = asyncio.run(use_case.execute(request))
    assert result is not None
    assert result.normalized_title == "Test Book"
