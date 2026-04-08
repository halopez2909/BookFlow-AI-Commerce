from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from main import app
from app.infrastructure.database import get_db

client = TestClient(app)


def override_get_db():
    yield MagicMock()


app.dependency_overrides[get_db] = override_get_db


def test_register_book_missing_required_fields():
    response = client.post("/catalog/books", json={
        "title": "Test Book",
    })
    assert response.status_code == 422


def test_register_book_invalid_isbn():
    response = client.post("/catalog/books", json={
        "title": "Test Book",
        "author": "Author",
        "publisher": "Publisher",
        "category_id": "00000000-0000-0000-0000-000000000001",
        "isbn": "123",
    })
    assert response.status_code == 422


def test_register_book_invalid_issn():
    response = client.post("/catalog/books", json={
        "title": "Test Book",
        "author": "Author",
        "publisher": "Publisher",
        "category_id": "00000000-0000-0000-0000-000000000001",
        "issn": "12345678",
    })
    assert response.status_code == 422
