import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.routers.normalization_router import router
from app.infrastructure.database import engine
from app.infrastructure.models import Base

load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Normalization Service",
    description="Servicio de limpieza y normalizacion de datos bibliograficos",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/health")
def health():
    return {"status": "ok", "service": "normalization-service"}
