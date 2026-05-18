import os
import sys

# Esta línea le dice a Python que busque dentro de la carpeta actual
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.routers.recommender_router import router as recommender_router

load_dotenv()

app = FastAPI(title="BookFlow Recommender Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(recommender_router)

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "recommender-service"}