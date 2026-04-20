import pytest
from app.domain.normalizers import TitleNormalizer


def test_normalize_title_sentence_case():
    n = TitleNormalizer()
    assert n.normalize("THE GREAT GATSBY") == "The great gatsby"


def test_normalize_title_removes_double_spaces():
    n = TitleNormalizer()
    result = n.normalize("El  senor  de  los  anillos")
    assert "  " not in result


def test_normalize_title_empty():
    n = TitleNormalizer()
    assert n.normalize("") == ""


def test_normalize_title_strips_whitespace():
    n = TitleNormalizer()
    result = n.normalize("  Don Quixote  ")
    assert not result.startswith(" ")
    assert not result.endswith(" ")
