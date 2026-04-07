# frontend-bookflow-admin

Panel administrativo de BookFlow AI Commerce (Frontend)

Resumen
- Frontend React + TypeScript (Vite) para administrar cargas masivas de inventario, ver lotes, errores, subir archivos y editar parámetros.
- Incluye un mock BFF (mock-bff.cjs) para desarrollo local y demo.
- Objetivo del repo: entregar MVP del panel administrativo para Sprint 1.

Contenido relevante
- src/ : código frontend (páginas, componentes, hooks, services)
- src/services/apiClient.ts : adaptador Axios + interceptores (JWT + toasts)
- src/context/AuthContext.tsx : sesión en memoria (AuthContext)
- src/hooks/ : useInventoryBatches, useBatchErrors, useConfigParams, etc.
- src/components/inventory/ : BatchTable, ErrorsTable, FileUploader
- mock-bff.cjs : servidor mock local (endpoints de prueba)
- batches.json : persistencia simple del mock
- Dockerfile, mock/Dockerfile, docker-compose.yml : para demo con Docker
- .env.example : ejemplo de variables de entorno

Prerequisitos
- Node.js 18+
- npm
- Git (recomendado)
- Docker Desktop (opcional para docker-compose)
- VS Code u otro editor

Variables de entorno
- Copiar `.env.example` a `.env` y ajustar si hace falta.
- Variable necesaria:
  - VITE_BFF_URL=http://localhost:8000

Instalación y ejecución local (sin Docker)
1. Clonar y entrar al repo:
```bash
git clone <repo-url>
cd frontend-bookflow-admin

1 Instalar dependencias:
npm install

2 Preparar .env:
cp .env.example .env
# o en PowerShell
Set-Content -Path .env -Value 'VITE_BFF_URL=http://localhost:8000' -Encoding utf8

3 Levantar mock BFF (en otra terminal):
node mock-bff.cjs

4 Levantar frontend:
npm run dev

Abrir en navegador:
Frontend: http://localhost:5173
Mock: http://localhost:8000
Usuario de prueba:
Usuario: demo
Contraseña: cualquiera
Endpoints mock (desarrollo)

POST /api/auth/login -> { token, user }
GET /api/inventory/batches -> [ImportBatch]
GET /api/inventory/batches/:id/errors -> [BatchError]
POST /api/inventory/upload -> ImportBatch (multipart)
DELETE /api/inventory/batches/:id -> { message, removed }
GET /health -> { status: 'ok' }
GET /api/config/params -> { ... } (AdminConfig)
PUT /api/config/params -> { ... }
Modelos (resumen)

ImportBatch:
id, file_name, upload_date, processed_rows, valid_rows, invalid_rows, status
BatchError:
id, row_number, error_type, message, fix_hint
Flujos principales (cómo probar manualmente)

Login:
/login -> POST /api/auth/login -> redirige a /admin/batches
Carga de inventario:
/admin/batches -> FileUploader -> POST /api/inventory/upload -> refetch GET /api/inventory/batches
Ver errores:
Click en lote -> /admin/batches/{id}/errors -> GET /api/inventory/batches/:id/errors
Eliminar lote:
Botón "Eliminar" en la tabla -> DELETE /api/inventory/batches/:id -> refetch
Configuración:
/admin/config -> GET /api/config/params -> editar -> PUT /api/config/params
Docker (levantar con Docker Desktop)

5 Asegúrarse .env en UTF‑8 sin BOM:
VITE_BFF_URL=http://localhost:8000

6 Construir y levantar:
docker compose build
docker compose up -d

7 Ver logs:
docker compose logs -f frontend
docker compose logs -f mock

8 Parar:
docker compose down

En docker-compose.yml el servicio frontend usa VITE_BFF_URL=http://mock:8000 para comunicación intra-Red Docker.
Si estás en entorno con proxy, puede ser necesario desactivar temporalmente variables HTTP_PROXY/HTTPS_PROXY durante el build o configurar proxy en Docker Desktop.
Toasts y manejo de errores

Integrado react-toastify para notificaciones.
apiClient muestra toasts de error por defecto (excepto 401 que redirige al login).
Para suprimir toasts en llamadas específicas, pasar { silent: true } en el config del request.
Pruebas (Vitest)

Ejecutar tests:
npm run test

Recomendado testear:
BatchTable (renderización)
ErrorsTable
FileUploader (validaciones)
Se recomienda usar MSW o mocks para endpoints en tests.
Buenas prácticas

No guardar token en localStorage en esta versión (token en memoria en AuthContext).
Mantener .env.example en el repo y no commitear .env.
Crear ramas feature/<ticket> y abrir PRs con descripción y pasos para probar.
Troubleshooting (problemas ya conocidos)

.env con caracteres extraños: recrear .env en UTF‑8 sin BOM.
Vite muestra HTML en vez de JSON: revisar apiClient.baseURL (ver consola, API baseURL=...).
Docker build RST_STREAM / INTERNAL_ERROR: reiniciar Docker Desktop, limpiar builder (docker builder prune), desactivar BuildKit temporalmente (DOCKER_BUILDKIT=0) o ajustar proxy.
Problemas de encoding en archivos .tsx: guardar en UTF‑8.
Desarrollo y estructura de carpetas (rápida)

src/
main.tsx, App.tsx, routes.tsx
context/AuthContext.tsx
services/apiClient.ts
hooks/useInventoryBatches.ts, useBatchErrors.ts, useConfigParams.ts
pages/admin/AdminBatches.tsx, BatchDetail.tsx, AdminConfig.tsx
components/inventory/BatchTable.tsx, ErrorsTable.tsx, FileUploader.tsx
mock-bff.cjs, batches.json
Dockerfile, mock/Dockerfile, docker-compose.yml
Contacto / responsables

Dev4 (Mock & Docker): Juan Sebastian Rodriguez Jimenez
Dev8 (Toasts & errores): Juan Sebastian Rodriguez Jimenez
Para incidencias: abrir un Issue con logs y pasos para reproducir.
Licencia

(Agregar licencia si aplica)