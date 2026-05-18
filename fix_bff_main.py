content = """import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

load_dotenv()

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:5173,http://localhost:5174").split(",")

app = FastAPI(title="BFF BookFlow", version="2.0.0")

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

@app.get("/health")
def health():
    return {"status": "ok", "service": "bff-bookflow"}
"""
with open('bff-bookflow/main.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done')
