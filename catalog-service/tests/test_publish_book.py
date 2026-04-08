from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from main import app
from app.infrastructure.database import get_db

client = TestClient(app)


def override_get_db():
    yield MagicMock()


app.dependency_overrides[get_db] = override_get_db


def test_publish_book_not_found(mocker):
    mocker.patch(
        "app.infrastructure.repositories.BookRepositoryPostgres.get_by_id",
        return_value=None,
    )
    response = client.post("/catalog/books/00000000-0000-0000-0000-000000000001/publish")
    assert response.status_code == 404
