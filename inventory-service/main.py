from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.inventory_router import router as inventory_router
from app.routers.data_quality_router import router as data_quality_router
from app.infrastructure.database import create_tables

app = FastAPI(title="Inventory Service", version="1.0.0")

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


app.include_router(inventory_router)
app.include_router(data_quality_router)


@app.get("/health")
def health():
    return {"status": "ok", "service": "inventory-service"}
