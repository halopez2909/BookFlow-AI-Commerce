from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from main import app
from app.infrastructure.database import get_db

client = TestClient(app)


def override_get_db():
    yield MagicMock()


app.dependency_overrides[get_db] = override_get_db


def test_upload_unsupported_format():
    response = client.post(
        "/inventory/upload",
        files={"file": ("test.pdf", b"fake content", "application/pdf")},
    )
    assert response.status_code == 400


def test_upload_empty_file():
    response = client.post(
        "/inventory/upload",
        files={"file": ("test.xlsx", b"", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
    )
    assert response.status_code == 400
