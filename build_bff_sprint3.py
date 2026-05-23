import os

# Cart router
cart_router = """from fastapi import APIRouter, Depends, HTTPException
import httpx
import os
from app.application.auth_middleware import validate_jwt

router = APIRouter(prefix="/api/cart", tags=["cart"])
CART_URL = os.getenv("CART_URL", "http://cart-service:8011")

@router.post("/items", status_code=201)
async def add_to_cart(data: dict):
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.post(f"{CART_URL}/cart/items", json=data)
            r.raise_for_status()
            return r.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{customer_id}")
async def get_cart(customer_id: str):
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(f"{CART_URL}/cart/{customer_id}")
            r.raise_for_status()
            return r.json()
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/items/{item_id}")
async def update_cart_item(item_id: int, data: dict):
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.put(f"{CART_URL}/cart/items/{item_id}", json=data)
            r.raise_for_status()
            return r.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/items/{item_id}")
async def remove_cart_item(item_id: int):
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.delete(f"{CART_URL}/cart/items/{item_id}")
            r.raise_for_status()
            return r.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{customer_id}")
async def clear_cart(customer_id: str):
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.delete(f"{CART_URL}/cart/{customer_id}")
            r.raise_for_status()
            return r.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
"""

# Orders router
orders_router = """from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
import httpx
import os
from app.application.auth_middleware import validate_jwt

router = APIRouter(prefix="/api/orders", tags=["orders"])
ORDER_URL = os.getenv("ORDER_URL", "http://order-service:8010")

@router.post("", status_code=201)
async def create_order(data: dict, payload: dict = Depends(validate_jwt)):
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.post(f"{ORDER_URL}/orders", json=data)
            r.raise_for_status()
            return r.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("")
async def get_orders(customer_id: Optional[str] = None, payload: dict = Depends(validate_jwt)):
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            params = {"customer_id": customer_id} if customer_id else {}
            r = await client.get(f"{ORDER_URL}/orders", params=params)
            r.raise_for_status()
            return r.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{order_id}")
async def get_order(order_id: str, payload: dict = Depends(validate_jwt)):
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(f"{ORDER_URL}/orders/{order_id}")
            r.raise_for_status()
            return r.json()
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/{order_id}/status")
async def update_order_status(order_id: str, data: dict, payload: dict = Depends(validate_jwt)):
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.put(f"{ORDER_URL}/orders/{order_id}/status", json=data)
            r.raise_for_status()
            return r.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
"""

# Assistant router
assistant_router = """from fastapi import APIRouter, HTTPException
import httpx
import os

router = APIRouter(prefix="/api/assistant", tags=["assistant"])
ASSISTANT_URL = os.getenv("ASSISTANT_URL", "http://ai-assistant-service:8012")

@router.post("/query")
async def query_assistant(data: dict):
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.post(f"{ASSISTANT_URL}/assistant/query", json=data)
            r.raise_for_status()
            return r.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sessions/{session_id}")
async def get_session(session_id: str):
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(f"{ASSISTANT_URL}/assistant/sessions/{session_id}")
            r.raise_for_status()
            return r.json()
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
"""

# Recommendations router
recommendations_router = """from fastapi import APIRouter, HTTPException
from typing import Optional
import httpx
import os

router = APIRouter(prefix="/api/recommendations", tags=["recommendations"])
RECOMMENDER_URL = os.getenv("RECOMMENDER_URL", "http://recommender-service:8090")

@router.get("/popular")
async def get_popular():
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(f"{RECOMMENDER_URL}/recommendations/popular")
            r.raise_for_status()
            return r.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{book_id}")
async def get_recommendations(book_id: str, strategy: Optional[str] = None):
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            params = {"strategy": strategy} if strategy else {}
            r = await client.get(f"{RECOMMENDER_URL}/recommendations/{book_id}", params=params)
            r.raise_for_status()
            return r.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
"""

# Write routers
with open("bff-bookflow/app/routers/cart_router.py", "w", encoding="utf-8") as f:
    f.write(cart_router)
print("cart_router.py creado")

with open("bff-bookflow/app/routers/orders_router.py", "w", encoding="utf-8") as f:
    f.write(orders_router)
print("orders_router.py creado")

with open("bff-bookflow/app/routers/assistant_router.py", "w", encoding="utf-8") as f:
    f.write(assistant_router)
print("assistant_router.py creado")

with open("bff-bookflow/app/routers/recommendations_router.py", "w", encoding="utf-8") as f:
    f.write(recommendations_router)
print("recommendations_router.py creado")

# Update main.py
main_py = """import os
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
from app.routers.cart_router import router as cart_router
from app.routers.orders_router import router as orders_router
from app.routers.assistant_router import router as assistant_router
from app.routers.recommendations_router import router as recommendations_router

load_dotenv()
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:5173,http://localhost:5174").split(",")

app = FastAPI(title="BFF BookFlow", version="3.0.0")
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
app.include_router(cart_router)
app.include_router(orders_router)
app.include_router(assistant_router)
app.include_router(recommendations_router)

@app.get("/health")
def health():
    return {"status": "ok", "service": "bff-bookflow"}
"""

with open("bff-bookflow/main.py", "w", encoding="utf-8") as f:
    f.write(main_py)
print("main.py actualizado")

# Update BFF .env
bff_env = open("bff-bookflow/.env", "r", encoding="utf-8").read()
additions = ""
if "CART_URL" not in bff_env:
    additions += "CART_URL=http://cart-service:8011\n"
if "ORDER_URL" not in bff_env:
    additions += "ORDER_URL=http://order-service:8010\n"
if "ASSISTANT_URL" not in bff_env:
    additions += "ASSISTANT_URL=http://ai-assistant-service:8012\n"
if "RECOMMENDER_URL" not in bff_env:
    additions += "RECOMMENDER_URL=http://recommender-service:8090\n"

if additions:
    with open("bff-bookflow/.env", "a", encoding="utf-8") as f:
        f.write("\n" + additions)
    print("BFF .env actualizado")
