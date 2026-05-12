# BookFlow-AI-Commerce — Sprint 3, Dev 6 (Jenn)

Rama de **evidencia** del Sprint 3 de Jennifer (Dev 6 — BFF Avanzado).

## Contenido

- `bff-bookflow/` — BFF actualizado con todas las rutas Sprint 3:
  - Routers: cart, orders, assistant, recommender, books-full, system, health
  - Clients (Adapter Pattern): cart_client, order_client, assistant_client, recommender_client, pricing_client
  - Tests pytest: 18/18 verdes
- `docker-compose.yml` — actualizado para incluir el BFF Sprint 3
- `init-db.sh` — script de inicializacion de DBs

## Patrones aplicados

- **Gateway Pattern** — el BFF es el unico punto de entrada del frontend
- **Facade Pattern** — `GET /api/books/{id}/full` agrega 4 servicios en una sola respuesta
- **Parallel Execution** — `asyncio.gather` ejecuta las 4 llamadas del endpoint full en paralelo
- **Throttling Pattern** — `slowapi` aplica rate limiting (100/min publico, 300/min autenticado)
- **Adapter Pattern** — un client dedicado por servicio (SRP)

## Como probar

```bash
cd bff-bookflow
pip install -r requirements.txt
pytest tests/ -v
# 18 tests passed

uvicorn main:app --reload
# Abrir http://localhost:8000/docs para ver todas las rutas Sprint 3
```

## Endpoints nuevos Sprint 3

| Metodo | Ruta | Auth |
|--------|------|------|
| POST   | /api/cart/items                       | JWT |
| GET    | /api/cart/{customer_id}               | JWT |
| PUT    | /api/cart/items/{item_id}             | JWT |
| DELETE | /api/cart/items/{item_id}             | JWT |
| POST   | /api/orders                           | JWT |
| GET    | /api/orders                           | JWT |
| GET    | /api/orders/{order_id}                | JWT |
| PUT    | /api/orders/{order_id}/status         | JWT |
| POST   | /api/assistant/query                  | publico |
| GET    | /api/assistant/sessions/{session_id}  | publico |
| GET    | /api/recommendations/popular          | publico |
| GET    | /api/recommendations/{book_id}        | publico |
| GET    | /api/books/{book_id}/full             | publico |
| GET    | /api/health                           | publico |
| GET    | /api/system/health                    | publico |
