import os

# -- normalization_client.py -----------------------------------------------
normalization_client = """import os
import httpx
from dotenv import load_dotenv

load_dotenv()
NORMALIZATION_URL = os.getenv('NORMALIZATION_URL', 'http://normalization-service:8005')


class NormalizationClient:
    async def normalize(self, data: dict) -> dict:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.post(f'{NORMALIZATION_URL}/normalization/normalize', json=data)
            r.raise_for_status()
            return r.json()

    async def normalize_batch(self, records: list) -> dict:
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.post(f'{NORMALIZATION_URL}/normalization/batch', json={'records': records})
            r.raise_for_status()
            return r.json()

    async def get_records(self) -> list:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(f'{NORMALIZATION_URL}/normalization/records')
            r.raise_for_status()
            return r.json()

    async def health(self) -> dict:
        async with httpx.AsyncClient(timeout=5) as client:
            r = await client.get(f'{NORMALIZATION_URL}/health')
            r.raise_for_status()
            return r.json()
"""

# -- pricing_client.py -----------------------------------------------------
pricing_client = """import os
import httpx
from dotenv import load_dotenv

load_dotenv()
PRICING_URL = os.getenv('PRICING_URL', 'http://pricing-service:8006')


class PricingClient:
    async def calculate(self, data: dict) -> dict:
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.post(f'{PRICING_URL}/pricing/calculate', json=data)
            r.raise_for_status()
            return r.json()

    async def get_decision(self, book_reference: str) -> dict:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(f'{PRICING_URL}/pricing/decisions/{book_reference}')
            r.raise_for_status()
            return r.json()

    async def health(self) -> dict:
        async with httpx.AsyncClient(timeout=5) as client:
            r = await client.get(f'{PRICING_URL}/health')
            r.raise_for_status()
            return r.json()
"""

# -- audit_client.py -------------------------------------------------------
audit_client = """import os
import httpx
from dotenv import load_dotenv

load_dotenv()
AUDIT_URL = os.getenv('AUDIT_URL', 'http://audit-service:8007')


class AuditClient:
    async def get_summary(self, book_reference: str) -> dict:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(f'{AUDIT_URL}/audit/summary/{book_reference}')
            r.raise_for_status()
            return r.json()

    async def get_pricing_audit(self, book_reference: str) -> dict:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(f'{AUDIT_URL}/audit/pricing/{book_reference}')
            r.raise_for_status()
            return r.json()

    async def get_enrichment_audit(self, book_reference: str) -> dict:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(f'{AUDIT_URL}/audit/enrichment/{book_reference}')
            r.raise_for_status()
            return r.json()

    async def health(self) -> dict:
        async with httpx.AsyncClient(timeout=5) as client:
            r = await client.get(f'{AUDIT_URL}/health')
            r.raise_for_status()
            return r.json()
"""

# -- integration_client.py -------------------------------------------------
integration_client = """import os
import httpx
from dotenv import load_dotenv

load_dotenv()
INTEGRATION_URL = os.getenv('INTEGRATION_URL', 'http://integration-service:8008')


class IntegrationClient:
    async def trigger(self, batch_id: str) -> dict:
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.post(f'{INTEGRATION_URL}/integration/trigger/{batch_id}')
            r.raise_for_status()
            return r.json()

    async def external_health(self) -> dict:
        async with httpx.AsyncClient(timeout=5) as client:
            r = await client.get(f'{INTEGRATION_URL}/external/health')
            r.raise_for_status()
            return r.json()
"""

# -- normalization_router.py (BFF) -----------------------------------------
normalization_router = """from fastapi import APIRouter, Depends, HTTPException
from app.infrastructure.clients.normalization_client import NormalizationClient
from app.application.auth_middleware import validate_jwt

router = APIRouter(prefix='/api/normalization', tags=['normalization'])


@router.post('/normalize', status_code=201)
async def normalize(data: dict, payload: dict = Depends(validate_jwt)):
    try:
        client = NormalizationClient()
        return await client.normalize(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/batch', status_code=201)
async def normalize_batch(data: dict, payload: dict = Depends(validate_jwt)):
    try:
        client = NormalizationClient()
        return await client.normalize_batch(data.get('records', []))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/records')
async def get_records(payload: dict = Depends(validate_jwt)):
    try:
        client = NormalizationClient()
        return await client.get_records()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
"""

# -- pricing_router.py (BFF) -----------------------------------------------
pricing_router = """from fastapi import APIRouter, Depends, HTTPException
from app.infrastructure.clients.pricing_client import PricingClient
from app.application.auth_middleware import validate_jwt

router = APIRouter(prefix='/api/pricing', tags=['pricing'])


@router.post('/calculate', status_code=201)
async def calculate_price(data: dict, payload: dict = Depends(validate_jwt)):
    try:
        client = PricingClient()
        return await client.calculate(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/decisions/{book_reference}')
async def get_pricing_decision(book_reference: str, payload: dict = Depends(validate_jwt)):
    try:
        client = PricingClient()
        return await client.get_decision(book_reference)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
"""

# -- audit_router.py (BFF) -------------------------------------------------
audit_router = """from fastapi import APIRouter, Depends, HTTPException
from app.infrastructure.clients.audit_client import AuditClient
from app.application.auth_middleware import validate_jwt

router = APIRouter(prefix='/api/audit', tags=['audit'])


@router.get('/summary/{book_reference}')
async def get_audit_summary(book_reference: str, payload: dict = Depends(validate_jwt)):
    try:
        client = AuditClient()
        return await client.get_summary(book_reference)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get('/pricing/{book_reference}')
async def get_pricing_audit(book_reference: str, payload: dict = Depends(validate_jwt)):
    try:
        client = AuditClient()
        return await client.get_pricing_audit(book_reference)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get('/enrichment/{book_reference}')
async def get_enrichment_audit(book_reference: str, payload: dict = Depends(validate_jwt)):
    try:
        client = AuditClient()
        return await client.get_enrichment_audit(book_reference)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
"""

# -- integration_router.py (BFF) -------------------------------------------
integration_router = """from fastapi import APIRouter, Depends, HTTPException
from app.infrastructure.clients.integration_client import IntegrationClient
from app.application.auth_middleware import validate_jwt

router = APIRouter(prefix='/api/integration', tags=['integration'])


@router.post('/trigger/{batch_id}', status_code=201)
async def trigger_integration(batch_id: str, payload: dict = Depends(validate_jwt)):
    try:
        client = IntegrationClient()
        return await client.trigger(batch_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/external/health')
async def external_health():
    try:
        client = IntegrationClient()
        return await client.external_health()
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))
"""

# -- system_router.py (BFF) ------------------------------------------------
system_router = """import os
import httpx
from fastapi import APIRouter

router = APIRouter(prefix='/api/system', tags=['system'])

SERVICES = {
    'auth-service': os.getenv('AUTH_URL', 'http://auth-service:8001'),
    'inventory-service': os.getenv('INVENTORY_URL', 'http://inventory-service:8002'),
    'catalog-service': os.getenv('CATALOG_URL', 'http://catalog-service:8003'),
    'ai-enrichment-service': os.getenv('ENRICHMENT_URL', 'http://ai-enrichment-service:8004'),
    'normalization-service': os.getenv('NORMALIZATION_URL', 'http://normalization-service:8005'),
    'pricing-service': os.getenv('PRICING_URL', 'http://pricing-service:8006'),
}


@router.get('/health')
async def system_health():
    results = {}
    for name, url in SERVICES.items():
        try:
            async with httpx.AsyncClient(timeout=3) as client:
                r = await client.get(f'{url}/health')
                results[name] = {'status': 'ok', 'code': r.status_code}
        except Exception as e:
            results[name] = {'status': 'error', 'detail': str(e)}
    overall = 'ok' if all(v['status'] == 'ok' for v in results.values()) else 'degraded'
    return {'overall': overall, 'services': results}
"""

# -- indexes migration catalog_db ------------------------------------------
catalog_indexes = """from alembic import op
import sqlalchemy as sa

revision = 'idx001_catalog_sprint2'
down_revision = 'cbe2924489be'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_index('idx_books_isbn', 'books', ['isbn'], unique=False)
    op.create_index('idx_books_category_id', 'books', ['category_id'], unique=False)
    op.create_index('idx_books_published_flag', 'books', ['published_flag'], unique=False)


def downgrade() -> None:
    op.drop_index('idx_books_isbn', table_name='books')
    op.drop_index('idx_books_category_id', table_name='books')
    op.drop_index('idx_books_published_flag', table_name='books')
"""

# -- indexes migration enrichment_db --------------------------------------
enrichment_indexes = """from alembic import op
import sqlalchemy as sa

revision = 'idx002_enrichment_sprint2'
down_revision = '59dd653872b7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_index('idx_enrichment_requests_book_reference', 'enrichment_requests', ['book_reference'], unique=False)


def downgrade() -> None:
    op.drop_index('idx_enrichment_requests_book_reference', table_name='enrichment_requests')
"""

# -- tests -----------------------------------------------------------------
test_bff_sprint2 = """import pytest
from unittest.mock import AsyncMock, patch, MagicMock


def test_normalization_router_routes():
    from app.routers.normalization_router import router
    routes = [r.path for r in router.routes]
    assert '/api/normalization/normalize' in routes
    assert '/api/normalization/batch' in routes
    assert '/api/normalization/records' in routes


def test_pricing_router_routes():
    from app.routers.pricing_router import router
    routes = [r.path for r in router.routes]
    assert '/api/pricing/calculate' in routes
    assert '/api/pricing/decisions/{book_reference}' in routes


def test_audit_router_routes():
    from app.routers.audit_router import router
    routes = [r.path for r in router.routes]
    assert '/api/audit/summary/{book_reference}' in routes
    assert '/api/audit/pricing/{book_reference}' in routes
    assert '/api/audit/enrichment/{book_reference}' in routes


def test_integration_router_routes():
    from app.routers.integration_router import router
    routes = [r.path for r in router.routes]
    assert '/api/integration/trigger/{batch_id}' in routes


def test_system_router_routes():
    from app.routers.system_router import router
    routes = [r.path for r in router.routes]
    assert '/api/system/health' in routes


def test_normalization_client_exists():
    from app.infrastructure.clients.normalization_client import NormalizationClient
    client = NormalizationClient()
    assert hasattr(client, 'normalize')
    assert hasattr(client, 'normalize_batch')
    assert hasattr(client, 'get_records')


def test_pricing_client_exists():
    from app.infrastructure.clients.pricing_client import PricingClient
    client = PricingClient()
    assert hasattr(client, 'calculate')
    assert hasattr(client, 'get_decision')


def test_audit_client_exists():
    from app.infrastructure.clients.audit_client import AuditClient
    client = AuditClient()
    assert hasattr(client, 'get_summary')
    assert hasattr(client, 'get_pricing_audit')
    assert hasattr(client, 'get_enrichment_audit')


def test_integration_client_exists():
    from app.infrastructure.clients.integration_client import IntegrationClient
    client = IntegrationClient()
    assert hasattr(client, 'trigger')
    assert hasattr(client, 'external_health')
"""

# -- updated .env for BFF --------------------------------------------------
bff_env = """AUTH_URL=http://auth-service:8001
INVENTORY_URL=http://inventory-service:8002
CATALOG_URL=http://catalog-service:8003
ENRICHMENT_URL=http://ai-enrichment-service:8004
NORMALIZATION_URL=http://normalization-service:8005
PRICING_URL=http://pricing-service:8006
AUDIT_URL=http://audit-service:8007
INTEGRATION_URL=http://integration-service:8008
JWT_SECRET_KEY=supersecretkey123bookflow
JWT_ALGORITHM=HS256
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173,http://localhost:5174
"""

bff_env_example = """AUTH_URL=http://auth-service:8001
INVENTORY_URL=http://inventory-service:8002
CATALOG_URL=http://catalog-service:8003
ENRICHMENT_URL=http://ai-enrichment-service:8004
NORMALIZATION_URL=http://normalization-service:8005
PRICING_URL=http://pricing-service:8006
AUDIT_URL=http://audit-service:8007
INTEGRATION_URL=http://integration-service:8008
JWT_SECRET_KEY=your_secret_key
JWT_ALGORITHM=HS256
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
"""

files = {
    'bff-bookflow/app/infrastructure/clients/normalization_client.py': normalization_client,
    'bff-bookflow/app/infrastructure/clients/pricing_client.py': pricing_client,
    'bff-bookflow/app/infrastructure/clients/audit_client.py': audit_client,
    'bff-bookflow/app/infrastructure/clients/integration_client.py': integration_client,
    'bff-bookflow/app/routers/normalization_router.py': normalization_router,
    'bff-bookflow/app/routers/pricing_router.py': pricing_router,
    'bff-bookflow/app/routers/audit_router.py': audit_router,
    'bff-bookflow/app/routers/integration_router.py': integration_router,
    'bff-bookflow/app/routers/system_router.py': system_router,
    'bff-bookflow/tests/test_bff_sprint2.py': test_bff_sprint2,
    'bff-bookflow/.env': bff_env,
    'bff-bookflow/.env.example': bff_env_example,
    'catalog-service/alembic/versions/idx001_catalog_sprint2_indexes.py': catalog_indexes,
    'ai-enrichment-service/alembic/versions/idx002_enrichment_sprint2_indexes.py': enrichment_indexes,
}

for path, content in files.items():
    full = os.path.join(os.getcwd(), path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Created: {path}')

print('Dev 9 BFF Sprint 2 done!')
