import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from dotenv import load_dotenv
from app.routers.auth_router import router as auth_router
from app.routers.inventory_router import router as inventory_router
from app.routers.catalog_router import router as catalog_router
from app.routers.config_router import router as config_router
from app.routers.normalization_router import router as normalization_router
from app.routers.pricing_router import router as pricing_router
from app.routers.audit_router import router as audit_router
from app.routers.integration_router import router as integration_router
from app.routers.system_router import router as system_router
from app.routers.cart_router import router as cart_router
from app.routers.orders_router import router as orders_router
from app.routers.assistant_router import router as assistant_router
from app.routers.recommendations_router import router as recommendations_router

load_dotenv()

limiter = Limiter(key_func=get_remote_address, default_limits=["200/minute"])
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:5173,http://localhost:5174").split(",")

app = FastAPI(title="BFF BookFlow", version="3.0.0")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(inventory_router)
app.include_router(catalog_router)
app.include_router(config_router)
app.include_router(normalization_router)
app.include_router(pricing_router)
app.include_router(audit_router)
app.include_router(integration_router)
app.include_router(system_router)
app.include_router(cart_router)
app.include_router(orders_router)
app.include_router(assistant_router)
app.include_router(recommendations_router)

@app.get("/health")
def health():
    return {"status": "ok", "service": "bff-bookflow"}
