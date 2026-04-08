from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.enrichment_router import router as enrichment_router
from app.infrastructure.database import create_tables

app = FastAPI(title="AI Enrichment Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    create_tables()


app.include_router(enrichment_router)


@app.get("/health")
def health():
    return {"status": "ok", "service": "ai-enrichment-service"}
