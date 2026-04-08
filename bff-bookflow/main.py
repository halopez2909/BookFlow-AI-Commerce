import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.routers.auth_router import router as auth_router
from app.routers.inventory_router import router as inventory_router
from app.routers.catalog_router import router as catalog_router
from app.routers.config_router import router as config_router

load_dotenv()

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

app = FastAPI(title="BFF BookFlow", version="1.0.0")

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


@app.get("/health")
def health():
    return {"status": "ok", "service": "bff-bookflow"}
