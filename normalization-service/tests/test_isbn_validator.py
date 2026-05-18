import pytest
from app.domain.normalizers import ISBNValidator


def test_valid_isbn13():
    v = ISBNValidator()
    assert v.validate("9780743273565") is True


def test_invalid_isbn():
    v = ISBNValidator()
    assert v.validate("123") is False


def test_none_isbn():
    v = ISBNValidator()
    assert v.validate(None) is False


def test_empty_isbn():
    v = ISBNValidator()
    assert v.validate("") is False
