"""BFF BookFlow - Main app
Sprint 3 (Dev 6 Jenn): + cart, orders, assistant, recommender, books-full, rate limiting global.
"""
import os
import httpx
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

# Routers existentes (Sprint 1/2)
from app.routers.auth_router import router as auth_router
from app.routers.inventory_router import router as inventory_router
from app.routers.catalog_router import router as catalog_router
from app.routers.config_router import router as config_router
from app.routers.normalization_router import router as normalization_router
from app.routers.pricing_router import router as pricing_router
from app.routers.audit_router import router as audit_router
from app.routers.integration_router import router as integration_router
from app.routers.system_router import router as system_router

# Routers NUEVOS (Sprint 3 - Dev 6 Jenn)
from app.routers.cart_router import router as cart_router, limiter as global_limiter
from app.routers.order_router import router as order_router
from app.routers.assistant_router import router as assistant_router
from app.routers.recommender_router import router as recommender_router
from app.routers.books_full_router import router as books_full_router
from app.routers.health_router import router as health_router

load_dotenv()

ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:3000,http://localhost:5173,http://localhost:5174",
).split(",")

app = FastAPI(title="BFF BookFlow", version="3.0.0", description="BFF avanzado Sprint 3")

# Rate limiter global compartido por los routers
app.state.limiter = global_limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(httpx.HTTPStatusError)
async def httpx_status_handler(request: Request, exc: httpx.HTTPStatusError):
    return JSONResponse(
        status_code=exc.response.status_code,
        content={
            "error": True,
            "code": exc.response.status_code,
            "message": "Error en servicio interno",
            "detail": exc.response.text[:300],
            "service_path": str(exc.request.url),
        },
    )


@app.exception_handler(httpx.RequestError)
async def httpx_request_handler(request: Request, exc: httpx.RequestError):
    return JSONResponse(
        status_code=502,
        content={
            "error": True,
            "code": 502,
            "message": "Servicio interno no disponible",
            "detail": str(exc),
        },
    )


# Routers Sprint 1/2
app.include_router(auth_router)
app.include_router(inventory_router)
app.include_router(catalog_router)
app.include_router(config_router)
app.include_router(normalization_router)
app.include_router(pricing_router)
app.include_router(audit_router)
app.include_router(integration_router)
app.include_router(system_router)

# Routers Sprint 3 - Dev 6 Jenn
app.include_router(cart_router)
app.include_router(order_router)
app.include_router(assistant_router)
app.include_router(recommender_router)
app.include_router(books_full_router)
app.include_router(health_router)


@app.get("/health")
def health():
    return {"status": "ok", "service": "bff-bookflow", "version": "3.0.0"}
