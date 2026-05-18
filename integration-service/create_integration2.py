import os

# -- tests -----------------------------------------------------------------
test_flow = """import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from app.domain.entities import IntegrationFlow, FlowStatus, StepStatus


def test_create_flow():
    flow = IntegrationFlow.create("batch-001")
    assert flow.batch_id == "batch-001"
    assert flow.status == FlowStatus.PENDING
    assert len(flow.steps) == 4
    step_names = [s.step_name for s in flow.steps]
    assert "inventory" in step_names
    assert "enrichment" in step_names
    assert "normalization" in step_names
    assert "catalog" in step_names


def test_flow_step_complete():
    flow = IntegrationFlow.create("batch-001")
    step = flow.get_step("inventory")
    step.start()
    assert step.status == StepStatus.RUNNING
    assert step.started_at is not None
    step.complete()
    assert step.status == StepStatus.COMPLETED
    assert step.completed_at is not None


def test_flow_step_fail():
    flow = IntegrationFlow.create("batch-001")
    step = flow.get_step("enrichment")
    step.start()
    step.fail("Connection timeout")
    assert step.status == StepStatus.FAILED
    assert step.error_message == "Connection timeout"


def test_flow_update_status_completed():
    flow = IntegrationFlow.create("batch-001")
    for step in flow.steps:
        step.start()
        step.complete()
    flow.update_status()
    assert flow.status == FlowStatus.COMPLETED


def test_flow_update_status_partial():
    flow = IntegrationFlow.create("batch-001")
    flow.steps[0].start()
    flow.steps[0].complete()
    flow.steps[1].start()
    flow.steps[1].fail("Error")
    flow.steps[2].start()
    flow.steps[2].complete()
    flow.steps[3].start()
    flow.steps[3].complete()
    flow.update_status()
    assert flow.status == FlowStatus.PARTIAL


def test_flow_update_status_failed():
    flow = IntegrationFlow.create("batch-001")
    for step in flow.steps:
        step.start()
        step.fail("Error")
    flow.update_status()
    assert flow.status == FlowStatus.FAILED


def test_get_step_returns_correct_step():
    flow = IntegrationFlow.create("batch-001")
    step = flow.get_step("normalization")
    assert step is not None
    assert step.step_name == "normalization"


def test_get_step_returns_none_for_unknown():
    flow = IntegrationFlow.create("batch-001")
    step = flow.get_step("unknown_step")
    assert step is None
"""

test_clients = """import pytest
from app.infrastructure.clients import (
    InventoryClient, EnrichmentClient,
    NormalizationClient, CatalogClient
)


def test_inventory_client_exists():
    client = InventoryClient()
    assert hasattr(client, 'get_batch')
    assert hasattr(client, 'get_batch_items')


def test_enrichment_client_exists():
    client = EnrichmentClient()
    assert hasattr(client, 'enrich')


def test_normalization_client_exists():
    client = NormalizationClient()
    assert hasattr(client, 'normalize')


def test_catalog_client_exists():
    client = CatalogClient()
    assert hasattr(client, 'get_categories')
    assert hasattr(client, 'register_book')
"""

test_router = """import pytest
from app.routers.integration_router import router


def test_router_has_trigger_route():
    routes = [r.path for r in router.routes]
    assert "/integration/trigger/{batch_id}" in routes


def test_router_has_status_route():
    routes = [r.path for r in router.routes]
    assert "/integration/status/{batch_id}" in routes


def test_router_has_flows_route():
    routes = [r.path for r in router.routes]
    assert "/integration/flows" in routes


def test_router_has_health_route():
    routes = [r.path for r in router.routes]
    assert "/integration/health" in routes
"""

# -- alembic/env.py --------------------------------------------------------
alembic_env = """import os
import sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.infrastructure.models import Base

config = context.config
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
"""

alembic_mako = """from alembic import op
import sqlalchemy as sa

revision = \
down_revision = \
branch_labels = \
depends_on = \


def upgrade() -> None:
    \


def downgrade() -> None:
    \
"""

migration = """from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = 'int001_create_flows'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'integration_flows',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('batch_id', sa.String(), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('steps', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('total_books', sa.Integer(), nullable=True),
        sa.Column('processed_books', sa.Integer(), nullable=True),
        sa.Column('failed_books', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_integration_flows_batch_id', 'integration_flows', ['batch_id'])


def downgrade() -> None:
    op.drop_index('idx_integration_flows_batch_id', table_name='integration_flows')
    op.drop_table('integration_flows')
"""

files = {
    'tests/test_flow_entities.py': test_flow,
    'tests/test_clients.py': test_clients,
    'tests/test_router.py': test_router,
    'alembic/__init__.py': '',
    'alembic/env.py': alembic_env,
    'alembic/script.py.mako': alembic_mako,
    'alembic/versions/__init__.py': '',
    'alembic/versions/int001_create_integration_flows.py': migration,
}

for path, content in files.items():
    full = os.path.join(os.getcwd(), path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Created: {path}')

print('Integration service tests done!')
