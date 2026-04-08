from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '59dd653872b7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'enrichment_requests',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('book_reference', sa.String(), nullable=False),
        sa.Column('title', sa.String(), nullable=True),
        sa.Column('author', sa.String(), nullable=True),
        sa.Column('isbn', sa.String(), nullable=True),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('requested_at', sa.DateTime(), nullable=True),
        sa.Column('source_used', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_enrichment_requests_book_reference'), 'enrichment_requests', ['book_reference'])
    op.create_table(
        'enrichment_results',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('request_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('normalized_title', sa.String(), nullable=True),
        sa.Column('normalized_author', sa.String(), nullable=True),
        sa.Column('normalized_publisher', sa.String(), nullable=True),
        sa.Column('normalized_description', sa.String(), nullable=True),
        sa.Column('cover_url', sa.String(), nullable=True),
        sa.Column('metadata_json', postgresql.JSON(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_enrichment_results_request_id'), 'enrichment_results', ['request_id'])


def downgrade() -> None:
    op.drop_index(op.f('ix_enrichment_results_request_id'), table_name='enrichment_results')
    op.drop_table('enrichment_results')
    op.drop_index(op.f('ix_enrichment_requests_book_reference'), table_name='enrichment_requests')
    op.drop_table('enrichment_requests')
