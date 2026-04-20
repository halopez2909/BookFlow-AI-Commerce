import pytest
from app.domain.normalizers import AuthorNormalizer


def test_normalize_author_first_last():
    n = AuthorNormalizer()
    result = n.normalize("Gabriel Garcia Marquez")
    assert "Marquez" in result
    assert "," in result


def test_normalize_author_already_formatted():
    n = AuthorNormalizer()
    result = n.normalize("Fitzgerald, F. Scott")
    assert "Fitzgerald" in result


def test_normalize_author_removes_accents():
    n = AuthorNormalizer()
    result = n.normalize("Garcia Marquez, Gabriel")
    assert result == "Garcia Marquez, Gabriel"


def test_normalize_author_single_name():
    n = AuthorNormalizer()
    result = n.normalize("Voltaire")
    assert result == "Voltaire"
