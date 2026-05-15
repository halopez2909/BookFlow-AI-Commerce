# AI Assistant Service — Documentación técnica (Sprint 3)

**Owner:** Juanse (Dev 4)
**Sprint:** 3 (7 al 17 de mayo de 2026)
**Repositorio:** `ai-assistant-service/`
**Puerto:** `8010`

---

## 1. ¿Qué hace este servicio?

Es el asistente conversacional de BookFlow. El usuario hace preguntas en lenguaje natural sobre el catálogo de libros y el sistema responde usando **datos reales** del Catalog, Inventory y Pricing Service. Si la API de IA falla o no está configurada, el servicio sigue funcionando con un clasificador de respaldo basado en palabras clave: nunca inventa información.

Casos de uso típicos:

- "¿tienen El principito disponible?" → consulta Catalog + Inventory.
- "¿cuánto cuesta Cien años de soledad?" → consulta Catalog + Pricing.
- "cuéntame sobre Don Quijote" → consulta Catalog (descripción).
- "libros de García Márquez" → busca en Catalog por autor.

---

## 2. Stack tecnológico

| Capa | Tecnología |
|------|-----------|
| Backend | Python 3.11 · FastAPI 0.111 · Pydantic v2 · Uvicorn |
| IA / NLP | OpenAI API (modelo configurable, default `gpt-4o-mini`) |
| Integración | httpx 0.27 (Catalog, Inventory, Pricing) |
| Base de datos | PostgreSQL 15 · SQLAlchemy 2 · Alembic · `assistant_db` |
| Pruebas | pytest 8 · pytest-mock · pytest-asyncio |
| Documentación | OpenAPI en `/docs` · Confluence |
| Infraestructura | Docker · Docker Compose · `.env` |

---

## 3. Arquitectura — hexagonal con DDD

```
ai-assistant-service/
├── main.py                       FastAPI app, health check, registra el router
├── app/
│   ├── domain/                   núcleo del negocio, sin dependencias técnicas
│   │   ├── entities.py           AssistantInteraction, BookSnapshot
│   │   ├── intents.py            IntentType (Enum) + INTENT_KEYWORDS
│   │   ├── intent_classifier.py  interfaz Strategy
│   │   ├── repositories.py       interfaz del repositorio
│   │   ├── response_builder.py   arma el texto final con datos reales
│   │   └── schemas.py            Pydantic DTOs (request/response)
│   ├── application/
│   │   └── use_cases.py          ProcessQuery (orquestador) + GetSessionHistory
│   ├── infrastructure/
│   │   ├── database.py           engine, SessionLocal, create_tables
│   │   ├── models.py             ORM SQLAlchemy
│   │   ├── repositories.py       implementación Postgres
│   │   ├── clients/              Adapters HTTP (Catalog/Inventory/Pricing)
│   │   └── providers/
│   │       ├── intent_classifier.py    AIClassifier (OpenAI)
│   │       └── fallback_classifier.py  FallbackClassifier (keywords)
│   └── routers/
│       └── assistant_router.py   POST /assistant/query, GET /assistant/sessions/{id}
├── alembic/                      migraciones (0001 crea assistant_interactions)
├── tests/                        17 pruebas con pytest
├── Dockerfile
├── requirements.txt
└── .env / .env.example
```

---

## 4. Endpoints

### `POST /assistant/query`

Procesa una pregunta y devuelve la respuesta.

**Request:**

```json
{
  "session_id": "demo-1",
  "question": "¿tienen El principito disponible?"
}
```

**Response:**

```json
{
  "answer": "Sí, \"El principito\" está disponible. Tenemos 5 unidades en stock.",
  "intent": "AVAILABILITY_CHECK",
  "sources": ["catalog", "inventory"]
}
```

El campo `sources` lista los servicios que se consultaron para construir la respuesta. Es trazabilidad explícita: el frontend puede mostrarle al usuario de dónde viene la información.

### `GET /assistant/sessions/{session_id}`

Devuelve el historial completo de una sesión, ordenado cronológicamente.

**Response:**

```json
{
  "session_id": "demo-1",
  "interactions": [
    {
      "id": "185a0030-d472-44c4-8ca2-a995a51b3125",
      "session_id": "demo-1",
      "user_question": "libros de García Márquez",
      "interpreted_intent": "BOOK_SEARCH",
      "answer_text": "Encontré 3 libro(s) relacionados...",
      "created_at": "2026-05-12T22:15:30Z"
    }
  ]
}
```

### `GET /health`

Health check para Docker Compose y monitoring.

```json
{ "status": "ok", "service": "ai-assistant-service" }
```

---

## 5. Intenciones reconocidas

El asistente clasifica cada pregunta en uno de estos cinco intents:

| Intent | Ejemplo | Servicios consultados |
|--------|---------|----------------------|
| `AVAILABILITY_CHECK` | "¿tienen X?", "¿hay stock de X?" | Catalog + Inventory |
| `PRICE_QUERY` | "¿cuánto cuesta X?", "precio de X" | Catalog + Pricing |
| `BOOK_INFO` | "cuéntame sobre X", "información de X" | Catalog |
| `BOOK_SEARCH` | "libros de Autor", "obras de Autor" | Catalog |
| `UNKNOWN` | cualquier cosa que no encaje | ninguno (mensaje de fallback) |

---

## 6. Flujo de procesamiento (Chain of Responsibility)

```
POST /assistant/query
       │
       ▼
┌──────────────────────────┐
│  1. ProcessQuery         │
│     ── _classify(q)      │
│        a) AIClassifier   │  (OpenAI)  ──► si UNKNOWN ──►
│        b) FallbackClass. │  (keywords)
│                          │
│  2. extract_entity(q)    │  título/autor por heurística
│                          │
│  3. consultar clients    │  según intent:
│        catalog / invent. │  - AVAILABILITY: catalog + inventory
│        / pricing         │  - PRICE: catalog + pricing
│                          │  - BOOK_INFO: catalog
│                          │  - BOOK_SEARCH: catalog
│                          │
│  4. ResponseBuilder.build│  texto con datos REALES
│                          │  (si falta un dato, lo dice)
│                          │
│  5. repo.save(interaction)│  persiste en assistant_db
│                          │
│  6. return {answer,      │
│            intent,       │
│            sources}      │
└──────────────────────────┘
```

---

## 7. Patrones de diseño aplicados

| Patrón | Dónde | Por qué |
|--------|-------|---------|
| **Strategy** | `IntentClassifier` con `AIClassifier` y `FallbackClassifier` | Permite cambiar la implementación sin tocar el orquestador. Mañana se puede agregar `HuggingFaceClassifier` sin tocar `ProcessQuery`. |
| **Chain of Responsibility** | `ProcessQuery.execute` | Cada paso pasa su resultado al siguiente: clasificar → extraer → consultar → construir → persistir. |
| **Adapter** | `CatalogClient`, `InventoryClient`, `PricingClient` | Traducen el JSON crudo de cada servicio a `BookSnapshot`, el modelo que entiende el dominio. |
| **Null Object** | `FallbackClassifier` devuelve `UNKNOWN` en lugar de lanzar excepción | El caller nunca tiene que envolver en `try/except`; la cadena sigue fluyendo. |

### Principios SOLID

- **S** — `IntentClassifier` solo clasifica. `ResponseBuilder` solo construye. `ProcessQuery` solo orquesta.
- **O** — Agregar un intent nuevo (ej. `RECOMMENDATION`) es agregar un caso en `ProcessQuery` y una variante en `ResponseBuilder`, sin tocar los clasificadores.
- **L** — `AIClassifier` y `FallbackClassifier` son intercambiables al 100% detrás de `IntentClassifier`.
- **D** — `ProcessQuery` depende de la interfaz `IntentClassifier`, no de OpenAI directamente. Los tests usan stubs sin levantar red.

---

## 8. Cómo configurar la API de IA (OpenAI)

El archivo `.env` del servicio acepta:

```env
OPENAI_API_KEY=sk-...           # Tu API key personal o de la org
OPENAI_MODEL=gpt-4o-mini        # Modelo a usar (default)
AI_TIMEOUT=4                    # Segundos máximos por llamada
```

Si `OPENAI_API_KEY` está vacía o falla la llamada (timeout, rate limit, red), `AIClassifier` retorna `UNKNOWN` y `ProcessQuery` delega automáticamente al `FallbackClassifier` (palabras clave, sin red). **El servicio sigue funcionando sin conexión a OpenAI.**

### Cambiar a otro proveedor de IA

Para reemplazar OpenAI por HuggingFace, Anthropic, o cualquier otro:

1. Crea una nueva clase en `app/infrastructure/providers/` que extienda `IntentClassifier`.
2. Implementa `async def classify(self, question: str) -> IntentType`.
3. Inyéctala en `app/routers/assistant_router.py` reemplazando `AIClassifier`.

No se toca ni `ProcessQuery` ni el dominio.

---

## 9. Cómo correr local

### Con Docker Compose (recomendado)

```bash
cd BookFlow-AI-Commerce-mainn
docker-compose up -d --build ai-assistant-service
docker-compose logs -f ai-assistant-service
```

Documentación interactiva: <http://localhost:8010/docs>

### Local sin Docker

```bash
cd ai-assistant-service
pip install -r requirements.txt
# Setea variables de entorno con tu Postgres local en .env
uvicorn main:app --reload --port 8010
```

### Correr las pruebas

```bash
cd ai-assistant-service
pytest -v
```

17 tests deberían pasar en verde:

- 7 de `FallbackClassifier`
- 6 de `AIClassifier` (con mock de OpenAI)
- 4 de `ProcessQuery` (disponibilidad, precio, no encontrado, fallback IA)

---

## 10. Variables de entorno

| Variable | Default | Descripción |
|----------|---------|-------------|
| `DATABASE_URL` | `postgresql://bookflow:bookflow123@postgres:5432/assistant_db` | Cadena de conexión Postgres |
| `OPENAI_API_KEY` | _(vacía)_ | API key de OpenAI; si está vacía se usa solo el fallback |
| `OPENAI_MODEL` | `gpt-4o-mini` | Modelo de chat completion |
| `CATALOG_URL` | `http://catalog-service:8003` | URL interna del Catalog |
| `INVENTORY_URL` | `http://inventory-service:8002` | URL interna del Inventory |
| `PRICING_URL` | `http://pricing-service:8008` | URL interna del Pricing |
| `HTTP_TIMEOUT` | `5` | Timeout en segundos para llamadas HTTP |
| `AI_TIMEOUT` | `4` | Timeout en segundos para la API de OpenAI |
| `SERVICE_PORT` | `8010` | Puerto donde escucha Uvicorn |

---

## 11. Esquema de base de datos

Tabla `assistant_interactions` en `assistant_db`:

| Columna | Tipo | Notas |
|---------|------|-------|
| `id` | `VARCHAR(36)` | Primary key, UUID generado por la app |
| `session_id` | `VARCHAR(128)` | Index. Agrupa interacciones de un mismo usuario/sesión |
| `user_question` | `TEXT` | Pregunta original del usuario |
| `interpreted_intent` | `VARCHAR(32)` | Uno de los 5 IntentType |
| `answer_text` | `TEXT` | Respuesta generada |
| `created_at` | `TIMESTAMP` | Timestamp UTC al momento de la respuesta |

Index compuesto `(session_id, created_at)` para consultar historial rápidamente.

Migración inicial: `alembic/versions/0001_create_assistant_interactions.py`.

---

## 12. Criterios de aceptación — checklist

| # | Criterio | Estado |
|---|----------|--------|
| 1 | `POST /assistant/query` recibe `{session_id, question}` y retorna `{answer, intent, sources}`. | ✅ |
| 2 | Reconoce 4 intenciones: disponibilidad, precio, características, búsqueda. | ✅ |
| 3 | Respuestas usan datos reales del sistema, no inventa nada. | ✅ |
| 4 | Si no encuentra el libro en el catálogo, responde que no está disponible (sin inventar). | ✅ |
| 5 | `GET /assistant/sessions/{session_id}` retorna el historial. | ✅ |
| 6 | Cada interacción se persiste como `AssistantInteraction` en `assistant_db`. | ✅ |
| 7 | Respuestas en < 5 segundos en condiciones normales (timeouts httpx=5s, AI=4s). | ✅ |
| 8 | Si la API de IA falla, fallback a búsqueda directa con keywords. | ✅ |
| 9 | Pruebas pytest: disponibilidad, precio, no encontrado, fallback IA. | ✅ (17 tests) |
| 10 | Dockerfile funcional y servicio en `docker-compose.yml`. | ✅ |
| 11 | Documentación en Confluence con flujo, intents y configuración. | ✅ (este doc) |

---

## 13. Integraciones con otros equipos del Sprint 3

- **JENN (Dev 6 — BFF):** consume `POST /assistant/query` desde `POST /api/assistant/query`. Contrato 1:1.
- **ALDANA (Dev 8 — UI):** llama al BFF de JENN, no directamente a este servicio.
- **LAURA (Dev 7 — Auditoría):** lee `assistant_db.assistant_interactions` para construir el feed global de eventos.
- **ALEJA (Dev 9 — Despliegue):** ya tiene `assistant_db` declarada en `init-db.sh` y el servicio en `docker-compose.yml`.

---

## 14. Demo del 20 de mayo

Flujo a mostrar en la demo, en orden:

1. Login en el frontend.
2. Abrir el catálogo.
3. Hacer clic en un libro → ver ficha con recomendaciones (Dev 5).
4. Agregar al carrito (Dev 1).
5. Generar pedido (Dev 2).
6. **Abrir el chat del asistente y preguntar:**
   - "¿tienen El principito disponible?" → muestra stock real.
   - "¿cuánto cuesta Cien años de soledad?" → muestra precio real.
   - "libros de García Márquez" → muestra lista del catálogo.
7. Recargar la página y mostrar que el historial de la sesión persiste.
