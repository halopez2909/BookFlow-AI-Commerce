from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.books_router import router as books_router
from app.routers.categories_router import router as categories_router
from app.infrastructure.database import create_tables

app = FastAPI(title="Catalog Service", version="1.0.0")

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


app.include_router(books_router)
app.include_router(categories_router)


@app.get("/health")
def health():
    return {"status": "ok", "service": "catalog-service"}
