from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.audit_router import router as audit_router
from app.infrastructure.database import create_tables

app = FastAPI(title="Audit Service", version="2.0.0", description="Sprint 3 — Auditoría Global del Sistema")

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


app.include_router(audit_router)


@app.get("/health")
def health():
    return {"status": "ok", "service": "audit-service", "version": "2.0.0"}
