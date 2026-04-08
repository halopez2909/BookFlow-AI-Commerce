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


def test_register_success(mocker):
    mocker.patch(
        "app.infrastructure.repositories.UserRepositoryPostgres.get_by_email",
        return_value=None,
    )
    mocker.patch(
        "app.infrastructure.repositories.UserRepositoryPostgres.save",
        return_value=MagicMock(
            id="00000000-0000-0000-0000-000000000001",
            email="test@test.com",
            role="user",
        ),
    )
    response = client.post("/auth/register", json={
        "email": "test@test.com",
        "password": "password123",
        "role": "user",
    })
    assert response.status_code == 201


def test_register_password_too_short():
    response = client.post("/auth/register", json={
        "email": "test@test.com",
        "password": "123",
        "role": "user",
    })
    assert response.status_code == 422


def test_register_invalid_email():
    response = client.post("/auth/register", json={
        "email": "not-an-email",
        "password": "password123",
        "role": "user",
    })
    assert response.status_code == 422
