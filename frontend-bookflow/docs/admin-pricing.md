# Panel de Administración — Pricing

Ruta: `/admin/pricing`
Autor: Dev 4 (Frontend)
Sprint: Pricing con IA

---

## 1. Objetivo

Dotar a los administradores de BookFlow de un panel visual donde revisar los precios sugeridos por el motor de IA para cada libro en stock, entender la justificación ("explanation") detrás de cada sugerencia, ajustar manualmente cuando corresponda, y forzar un recálculo puntual por libro.

Este documento describe la implementación del panel, las convenciones arquitectónicas, los contratos de API esperados y los procedimientos para correr, testear y buildear el módulo.

---

## 2. Alcance del sprint

### Week 1 — Mocks locales (estado actual)

La UI está completa y funcionando con **mocks locales** definidos en `src/pages/admin/pricing/pricingMocks.ts`. Esto permite desarrollar y validar la experiencia sin bloquear a Dev 1 y Dev 2 mientras terminan los endpoints del BFF.

### Week 2 — Integración con BFF real

Un feature flag (`VITE_PRICING_USE_MOCKS`) controla si los hooks de React Query devuelven mocks o si golpean los endpoints reales del BFF. Cuando el backend esté listo, basta con poner el flag en `false` y redeployar — no se requieren cambios de código en el frontend.

---

## 3. Arquitectura y patrones

El módulo respeta las convenciones ya presentes en el resto del frontend:

**Custom Hook Pattern.** Toda la lógica de acceso a datos vive en hooks dedicados (`usePricingList`, `usePricingDetail`, `usePricingOverride`, `usePricingRecalculate`). Los componentes nunca instancian `axios` ni tocan el query client directamente.

**Container / Presentational.** La página `AdminPricing` actúa como container (compone hooks, decide qué mostrar), mientras que los componentes bajo `src/components/pricing/` son presentacionales puros (reciben props, renderizan, emiten callbacks).

**Adapter.** Todas las requests pasan por `src/services/apiClient.ts`, un `axios` preconfigurado con `baseURL` y el interceptor de token registrado desde `AuthContext`. El resto de la app no conoce `axios` directamente.

**Command Query Separation (CQS).** Los hooks de lectura (`useQuery`) están separados de los de escritura (`useMutation`). Esto hace explícito el side-effect y facilita invalidar caché solo donde corresponde.

### SOLID aplicado

**Single Responsibility:** cada hook y cada componente tiene una sola razón de cambio. `PricingTable` solo dibuja filas; si cambia el shape del dato, cambia en `types.ts` y el adaptador, no en el componente.

**Open/Closed:** agregar un nuevo estado de pricing (por ejemplo `'archived'`) implica extender el union type en `types.ts` y agregar una entrada al `Record` de `PricingStatusBadge`. Ningún componente existente se modifica.

**Liskov Substitution:** `ExplanationPanel` maneja `PricingExplanation | string` mediante un type guard (`isStructured`). Cualquier consumidor que le pase cualquiera de los dos formatos funciona sin cambios.

**Interface Segregation:** los hooks exponen APIs mínimas. `usePricingOverride` devuelve solo `{ override, overrideAsync, isSaving, error }`; no filtra el `UseMutationResult` completo para no crear dependencias innecesarias.

**Dependency Inversion:** los componentes dependen de abstracciones (funciones callback, tipos) y no de implementaciones. `PricingTable` recibe `onRowClick` y `onRecalculate` como props; no sabe ni le importa si por debajo hay React Query, Redux o lo que sea.

---

## 4. Estructura de archivos

frontend-bookflow/
├── src/
│   ├── utils/
│   │   └── types.ts                          # PricingDecision, PricingExplanation, PricingStatus, PricingSource
│   ├── services/
│   │   └── apiClient.ts                      # axios preconfigurado (Adapter)
│   ├── hooks/
│   │   ├── usePricingList.ts                 # Query listado (mocks vs BFF según flag)
│   │   ├── usePricingDetail.ts               # Query detalle por id
│   │   ├── usePricingOverride.ts             # Mutation PUT /override
│   │   └── usePricingRecalculate.ts          # Mutation POST /calculate
│   ├── components/
│   │   └── pricing/
│   │       ├── PricingTable.tsx              # Tabla presentacional con 7 columnas
│   │       ├── PricingStatusBadge.tsx        # Badge coloreado por estado
│   │       ├── ExplanationPanel.tsx          # Panel lateral con justificación
│   │       └── PriceOverrideForm.tsx         # Form de ajuste manual con validación
│   └── pages/
│       └── admin/
│           └── pricing/
│               ├── AdminPricing.tsx          # Container (ruta /admin/pricing)
│               └── pricingMocks.ts           # Datos mock para Week 1
├── tests/
│   ├── PricingTable.test.tsx
│   ├── ExplanationPanel.test.tsx
│   └── PriceOverrideForm.test.tsx
├── docs/
│   └── admin-pricing.md                      # Este documento
├── vite.config.ts                            # incluye config de Vitest
├── nginx.conf                                # SPA fallback + cache de assets
└── Dockerfile                                # multi-stage build (node → nginx)

---

## 5. Tipos del dominio

Definidos en `src/utils/types.ts`:

```ts
type PricingStatus = 'suggested' | 'applied' | 'pending' | 'overridden'

type PricingSource = {
  name: string
  url?: string
  price?: number
}

type PricingExplanation = {
  summary: string
  factors?: string[]
  method?: string
  notes?: string
}

type PricingDecision = {
  id: string
  book_id: string
  title: string
  author: string
  condition: string
  suggested_price: number
  final_price?: number
  manual_price?: number
  currency?: string
  condition_factor: number
  reference_count: number
  sources: PricingSource[]
  explanation: PricingExplanation | string
  status: PricingStatus
  updated_at?: string
}
```

### Semántica de los estados (badges)

| Estado       | Cuándo aparece                                                           |
|--------------|--------------------------------------------------------------------------|
| `suggested`  | Recién calculado por IA, aún no aplicado al catálogo.                    |
| `applied`    | El precio sugerido fue aceptado y ya está publicado en el catálogo.      |
| `pending`    | La IA no pudo decidir con suficiente confianza, espera revisión humana.  |
| `overridden` | El admin sobreescribió el precio con un valor manual (`manual_price`).   |

---

## 6. Flujo de datos y contratos de API

El frontend consume cuatro endpoints del BFF. Los paths están documentados aquí como referencia para Dev 1 / Dev 2 que implementan el backend.

### 6.1 Listado

`GET /api/pricing/decisions`

**Response (200):** `PricingDecision[]`

Usado por el hook `usePricingList`. React Query key: `['pricing', 'list']`. `staleTime: 60s`.

### 6.2 Detalle

`GET /api/pricing/decisions/:id`

**Response (200):** `PricingDecision`

Usado por `usePricingDetail` cuando el admin abre una fila. Query key: `['pricing', 'detail', id]`. `enabled: !!id`.

### 6.3 Override manual

`PUT /api/pricing/decisions/:id/override`

**Request body:**

```json
{ "manual_price": 24500 }
```

**Response (200):** `PricingDecision` (con `status: 'overridden'` y `manual_price` poblado).

Usado por `usePricingOverride`. Al éxito, invalida `['pricing', 'list']` y `['pricing', 'detail', id]`, y emite un toast de confirmación. Al error, toast rojo con el mensaje del backend.

### 6.4 Recálculo puntual

`POST /api/pricing/calculate`

**Request body:**

```json
{ "decision_id": "pd-001" }
```

**Response (200):** `PricingDecision` (la nueva sugerencia de la IA).

Usado por `usePricingRecalculate`. Invalida el listado y el detalle. Mientras dura la mutación, el botón "Recalcular" de esa fila queda deshabilitado y muestra "Recalculando...".

---

## 7. Feature flag de mocks

La variable `VITE_PRICING_USE_MOCKS` en `.env` decide la fuente de datos:

```env
VITE_PRICING_USE_MOCKS=true     # Week 1: usa src/pages/admin/pricing/pricingMocks.ts
VITE_PRICING_USE_MOCKS=false    # Week 2+: golpea el BFF real vía apiClient
```

La lectura se hace con `import.meta.env.VITE_PRICING_USE_MOCKS === 'true'`. Al activar el BFF real, es suficiente con recargar Vite o redeployar el contenedor con el env actualizado — el código no se toca.

**Importante:** el archivo `.env` debe guardarse como **UTF-8 sin BOM**. En Windows con VS Code es el default; con `echo > .env` desde `cmd` se agrega un BOM que hace que Vite no lea la variable y la UI quede con datos vacíos.

---

## 8. Cómo correr localmente

Requisitos: Node ≥ 20, npm ≥ 10, `mock-bff.cjs` corriendo para login.

```bash
# Terminal 1 — BFF mock (auth + /api)
node mock-bff.cjs

# Terminal 2 — Frontend
cd frontend-bookflow
npm install
npm run dev
```

Abrir `http://localhost:5173`, loguearse con cualquier usuario (el mock-bff acepta todo), y navegar manualmente a `/admin/pricing` o vía el link en `/admin/batches`.

---

## 9. Tests

Stack: **Vitest** + **@testing-library/react** + **jsdom**.

```bash
npm run test       # watch mode (desarrollo)
npm run test:run   # corrida única (CI)
```

Cobertura actual del módulo de pricing (11 tests en 3 archivos):

- `PricingTable.test.tsx` (4): renderiza filas, muestra `manual_price` sobre `suggested_price`, dispara `onRowClick` al clickear fila, `onRecalculate` no burbujea la selección.
- `ExplanationPanel.test.tsx` (2): renderiza explanation string, renderiza explanation estructurado con sus secciones.
- `PriceOverrideForm.test.tsx` (5): error con input vacío, error con NaN, error con ≤0, llamada a `onSubmit(number)` con input válido, botón deshabilitado mientras guarda.

Setup de jsdom y matchers en `src/setupTests.ts`; configuración de Vitest (globals, environment, setupFiles) en `vite.config.ts`.

---

## 10. Build y despliegue

### Build local

```bash
npm run build        # genera dist/
npm run preview      # prueba el bundle
```

### Docker

```bash
docker build -t bookflow-frontend .
docker run --rm -p 8080:80 bookflow-frontend
```

El `Dockerfile` es multi-stage: primero compila el bundle con Node, luego lo sirve con `nginx:alpine`. La configuración de nginx (`nginx.conf`) incluye:

- **SPA fallback** (`try_files $uri $uri/ /index.html`) para que las rutas profundas como `/admin/pricing` no devuelvan 404 al navegar directo o al recargar.
- **Cache de assets versionados** (`/assets/` → `expires 1y, immutable`), aprovechando el hash que Vite agrega a los filenames.

El contenedor **no incluye backend**; el login y el `/api/*` requieren que se orqueste junto con el contenedor del BFF (responsabilidad de Dev 5 / infra).

---

## 11. Limitaciones conocidas y pendientes

**Auth en memoria.** El token se almacena solo en `AuthContext` (React state), no en `localStorage`. Al refrescar la página se pierde y el usuario vuelve al login. Esto se heredó de la implementación previa y excede el scope de este sprint. Ticket sugerido: persistir token con expiración en `sessionStorage`.

**Sin integración BFF real.** El flag queda en `true` hasta que Dev 1 / Dev 2 confirmen que los 4 endpoints están disponibles y respetan los contratos de la sección 6.

**Tests E2E pendientes.** Los tests actuales son unitarios (componentes aislados). No hay cobertura de flujo completo (entrar al panel, clickear fila, overridear, recalcular). Ticket sugerido: sumar Playwright o Cypress en un sprint siguiente.

**Accesibilidad.** `PriceOverrideForm` tiene `aria-label` y `role="alert"`, pero no se hizo una auditoría completa del panel con lectores de pantalla. Nice-to-have para una siguiente iteración.

------

## 5. Tipos del dominio

Definidos en `src/utils/types.ts`:

```ts
type PricingStatus = 'suggested' | 'applied' | 'pending' | 'overridden'

type PricingSource = {
  name: string
  url?: string
  price?: number
}

type PricingExplanation = {
  summary: string
  factors?: string[]
  method?: string
  notes?: string
}

type PricingDecision = {
  id: string
  book_id: string
  title: string
  author: string
  condition: string
  suggested_price: number
  final_price?: number
  manual_price?: number
  currency?: string
  condition_factor: number
  reference_count: number
  sources: PricingSource[]
  explanation: PricingExplanation | string
  status: PricingStatus
  updated_at?: string
}
```

### Semántica de los estados (badges)

| Estado       | Cuándo aparece                                                           |
|--------------|--------------------------------------------------------------------------|
| `suggested`  | Recién calculado por IA, aún no aplicado al catálogo.                    |
| `applied`    | El precio sugerido fue aceptado y ya está publicado en el catálogo.      |
| `pending`    | La IA no pudo decidir con suficiente confianza, espera revisión humana.  |
| `overridden` | El admin sobreescribió el precio con un valor manual (`manual_price`).   |

---

## 6. Flujo de datos y contratos de API

El frontend consume cuatro endpoints del BFF. Los paths están documentados aquí como referencia para Dev 1 / Dev 2 que implementan el backend.

### 6.1 Listado

`GET /api/pricing/decisions`

**Response (200):** `PricingDecision[]`

Usado por el hook `usePricingList`. React Query key: `['pricing', 'list']`. `staleTime: 60s`.

### 6.2 Detalle

`GET /api/pricing/decisions/:id`

**Response (200):** `PricingDecision`

Usado por `usePricingDetail` cuando el admin abre una fila. Query key: `['pricing', 'detail', id]`. `enabled: !!id`.

### 6.3 Override manual

`PUT /api/pricing/decisions/:id/override`

**Request body:**

```json
{ "manual_price": 24500 }
```

**Response (200):** `PricingDecision` (con `status: 'overridden'` y `manual_price` poblado).

Usado por `usePricingOverride`. Al éxito, invalida `['pricing', 'list']` y `['pricing', 'detail', id]`, y emite un toast de confirmación. Al error, toast rojo con el mensaje del backend.

### 6.4 Recálculo puntual

`POST /api/pricing/calculate`

**Request body:**

```json
{ "decision_id": "pd-001" }
```

**Response (200):** `PricingDecision` (la nueva sugerencia de la IA).

Usado por `usePricingRecalculate`. Invalida el listado y el detalle. Mientras dura la mutación, el botón "Recalcular" de esa fila queda deshabilitado y muestra "Recalculando...".

---

## 7. Feature flag de mocks

La variable `VITE_PRICING_USE_MOCKS` en `.env` decide la fuente de datos:

```env
VITE_PRICING_USE_MOCKS=true     # Week 1: usa src/pages/admin/pricing/pricingMocks.ts
VITE_PRICING_USE_MOCKS=false    # Week 2+: golpea el BFF real vía apiClient
```

La lectura se hace con `import.meta.env.VITE_PRICING_USE_MOCKS === 'true'`. Al activar el BFF real, es suficiente con recargar Vite o redeployar el contenedor con el env actualizado — el código no se toca.

**Importante:** el archivo `.env` debe guardarse como **UTF-8 sin BOM**. En Windows con VS Code es el default; con `echo > .env` desde `cmd` se agrega un BOM que hace que Vite no lea la variable y la UI quede con datos vacíos.

---

## 8. Cómo correr localmente

Requisitos: Node ≥ 20, npm ≥ 10, `mock-bff.cjs` corriendo para login.

```bash
# Terminal 1 — BFF mock (auth + /api)
node mock-bff.cjs

# Terminal 2 — Frontend
cd frontend-bookflow
npm install
npm run dev
```

Abrir `http://localhost:5173`, loguearse con cualquier usuario (el mock-bff acepta todo), y navegar manualmente a `/admin/pricing` o vía el link en `/admin/batches`.

---

## 9. Tests

Stack: **Vitest** + **@testing-library/react** + **jsdom**.

```bash
npm run test       # watch mode (desarrollo)
npm run test:run   # corrida única (CI)
```

Cobertura actual del módulo de pricing (11 tests en 3 archivos):

- `PricingTable.test.tsx` (4): renderiza filas, muestra `manual_price` sobre `suggested_price`, dispara `onRowClick` al clickear fila, `onRecalculate` no burbujea la selección.
- `ExplanationPanel.test.tsx` (2): renderiza explanation string, renderiza explanation estructurado con sus secciones.
- `PriceOverrideForm.test.tsx` (5): error con input vacío, error con NaN, error con ≤0, llamada a `onSubmit(number)` con input válido, botón deshabilitado mientras guarda.

Setup de jsdom y matchers en `src/setupTests.ts`; configuración de Vitest (globals, environment, setupFiles) en `vite.config.ts`.

---

## 10. Build y despliegue

### Build local

```bash
npm run build        # genera dist/
npm run preview      # prueba el bundle
```

### Docker

```bash
docker build -t bookflow-frontend .
docker run --rm -p 8080:80 bookflow-frontend
```

El `Dockerfile` es multi-stage: primero compila el bundle con Node, luego lo sirve con `nginx:alpine`. La configuración de nginx (`nginx.conf`) incluye:

- **SPA fallback** (`try_files $uri $uri/ /index.html`) para que las rutas profundas como `/admin/pricing` no devuelvan 404 al navegar directo o al recargar.
- **Cache de assets versionados** (`/assets/` → `expires 1y, immutable`), aprovechando el hash que Vite agrega a los filenames.

El contenedor **no incluye backend**; el login y el `/api/*` requieren que se orqueste junto con el contenedor del BFF (responsabilidad de Dev 5 / infra).

---

## 11. Limitaciones conocidas y pendientes

**Auth en memoria.** El token se almacena solo en `AuthContext` (React state), no en `localStorage`. Al refrescar la página se pierde y el usuario vuelve al login. Esto se heredó de la implementación previa y excede el scope de este sprint. Ticket sugerido: persistir token con expiración en `sessionStorage`.

**Sin integración BFF real.** El flag queda en `true` hasta que Dev 1 / Dev 2 confirmen que los 4 endpoints están disponibles y respetan los contratos de la sección 6.

**Tests E2E pendientes.** Los tests actuales son unitarios (componentes aislados). No hay cobertura de flujo completo (entrar al panel, clickear fila, overridear, recalcular). Ticket sugerido: sumar Playwright o Cypress en un sprint siguiente.

**Accesibilidad.** `PriceOverrideForm` tiene `aria-label` y `role="alert"`, pero no se hizo una auditoría completa del panel con lectores de pantalla. Nice-to-have para una siguiente iteración.

---

## 12. Contacto

Cualquier duda sobre esta implementación: Dev 4. Reportar bugs abriendo issue en el repo con el label `pricing-panel`.

