from alembic import op
import sqlalchemy as sa

revision = 'idx002_enrichment_sprint2'
down_revision = '59dd653872b7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_index('idx_enrichment_requests_book_reference', 'enrichment_requests', ['book_reference'], unique=False)


def downgrade() -> None:
    op.drop_index('idx_enrichment_requests_book_reference', table_name='enrichment_requests')
