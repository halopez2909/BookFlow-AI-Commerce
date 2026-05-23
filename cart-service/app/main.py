from fastapi import FastAPI

from app.infrastructure.database import create_tables
from app.routers.cart_router import router as cart_router

app = FastAPI(
    title="BookFlow Cart Service",
    description="Servicio de carrito de compras para Sprint 3.",
    version="1.0.0",
)


@app.on_event("startup")
def startup_event():
    create_tables()


@app.get("/health")
def health():
    return {
        "service": "cart-service",
        "status": "up",
    }


app.include_router(cart_router)
