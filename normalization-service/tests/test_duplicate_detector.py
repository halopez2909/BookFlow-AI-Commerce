import pytest
from unittest.mock import MagicMock
from app.domain.duplicate_detector import DuplicateDetector


def test_detect_duplicate():
    mock_db = MagicMock()
    mock_db.execute.return_value.fetchone.return_value = ("existing-id",)
    detector = DuplicateDetector(mock_db)
    is_dup, dup_id = detector.detect("9780743273565")
    assert is_dup is True
    assert dup_id == "existing-id"


def test_no_duplicate():
    mock_db = MagicMock()
    mock_db.execute.return_value.fetchone.return_value = None
    detector = DuplicateDetector(mock_db)
    is_dup, dup_id = detector.detect("9780743273565")
    assert is_dup is False
    assert dup_id is None


def test_no_isbn():
    mock_db = MagicMock()
    detector = DuplicateDetector(mock_db)
    is_dup, dup_id = detector.detect(None)
    assert is_dup is False
    assert dup_id is None
