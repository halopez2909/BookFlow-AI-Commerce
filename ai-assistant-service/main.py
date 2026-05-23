from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.assistant_router import router as assistant_router
from app.infrastructure.database import create_tables

app = FastAPI(
    title="AI Assistant Service",
    version="1.0.0",
    description="Asistente conversacional de BookFlow. Interpreta preguntas en "
                "lenguaje natural y responde con datos reales del catálogo, "
                "inventario y pricing.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    create_tables()


app.include_router(assistant_router)


@app.get("/health")
def health():
    return {"status": "ok", "service": "ai-assistant-service"}