from fastapi import FastAPI
from app.infrastructure.database import Base, engine
from app.routers import order_router

app = FastAPI(title="Order Service", version="1.0.0")

Base.metadata.create_all(bind=engine)

app.include_router(order_router.router)

@app.get("/health")
def health():
    return {"status": "ok", "service": "order-service"}
