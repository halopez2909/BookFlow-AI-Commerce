import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_me_without_token():
    response = client.get("/auth/me")
    assert response.status_code == 403


def test_get_me_with_invalid_token():
    response = client.get("/auth/me", headers={
        "Authorization": "Bearer invalidtoken123"
    })
    assert response.status_code == 401
