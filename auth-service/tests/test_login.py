import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from main import app
from app.infrastructure.database import get_db

client = TestClient(app)


def override_get_db():
    db = MagicMock()
    yield db


app.dependency_overrides[get_db] = override_get_db


def test_login_invalid_credentials(mocker):
    mocker.patch(
        "app.infrastructure.repositories.UserRepositoryPostgres.get_by_email",
        return_value=None,
    )
    response = client.post("/auth/login", json={
        "email": "wrong@test.com",
        "password": "wrongpassword",
    })
    assert response.status_code == 401


def test_login_missing_fields():
    response = client.post("/auth/login", json={
        "email": "test@test.com",
    })
    assert response.status_code == 422
