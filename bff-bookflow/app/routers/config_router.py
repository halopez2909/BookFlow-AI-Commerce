from fastapi import APIRouter, Depends
from app.infrastructure.clients.config_client import ConfigClient
from app.application.auth_middleware import validate_jwt

router = APIRouter(prefix="/api/config", tags=["config"])


@router.get("/params")
def get_params(payload: dict = Depends(validate_jwt)):
    client = ConfigClient()
    return client.get_params()


@router.put("/params")
def update_params(
    params: dict,
    payload: dict = Depends(validate_jwt),
):
    client = ConfigClient()
    return client.update_params(params)
