from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from main import app
from app.infrastructure.database import get_db

client = TestClient(app)


def override_get_db():
    yield MagicMock()


app.dependency_overrides[get_db] = override_get_db


def test_list_books_returns_200(mocker):
    mocker.patch(
        "app.infrastructure.repositories.BookRepositoryPostgres.find_all",
        return_value=([], 0),
    )
    response = client.get("/catalog/books")
    assert response.status_code == 200


def test_list_books_with_filters(mocker):
    mocker.patch(
        "app.infrastructure.repositories.BookRepositoryPostgres.find_all",
        return_value=([], 0),
    )
    response = client.get("/catalog/books?title=python&page=1&page_size=10")
    assert response.status_code == 200
