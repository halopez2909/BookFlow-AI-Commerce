import pytest
from app.infrastructure.google_books_client import GoogleBooksClient
from app.infrastructure.open_library_client import OpenLibraryClient
from app.infrastructure.crossref_client import CrossrefClient


def test_google_books_client_exists():
    client = GoogleBooksClient()
    assert hasattr(client, 'lookup')
    assert hasattr(client, 'health_check')


def test_open_library_client_exists():
    client = OpenLibraryClient()
    assert hasattr(client, 'lookup')
    assert hasattr(client, 'health_check')


def test_crossref_client_exists():
    client = CrossrefClient()
    assert hasattr(client, 'lookup_by_issn')
    assert hasattr(client, 'health_check')
