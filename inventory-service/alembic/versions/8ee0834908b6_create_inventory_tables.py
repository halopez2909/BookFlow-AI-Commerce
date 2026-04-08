from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '8ee0834908b6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'import_batches',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('file_name', sa.String(), nullable=False),
        sa.Column('upload_date', sa.DateTime(), nullable=True),
        sa.Column('total_rows', sa.Integer(), nullable=True),
        sa.Column('valid_rows', sa.Integer(), nullable=True),
        sa.Column('invalid_rows', sa.Integer(), nullable=True),
        sa.Column('status', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'inventory_items',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('external_code', sa.String(), nullable=False),
        sa.Column('book_reference', sa.String(), nullable=False),
        sa.Column('quantity_available', sa.Integer(), nullable=True),
        sa.Column('quantity_reserved', sa.Integer(), nullable=True),
        sa.Column('condition', sa.String(), nullable=False),
        sa.Column('defects', sa.String(), nullable=True),
        sa.Column('observations', sa.String(), nullable=True),
        sa.Column('import_batch_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(['import_batch_id'], ['import_batches.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_inventory_items_book_reference'), 'inventory_items', ['book_reference'])
    op.create_table(
        'import_errors',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('batch_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('row_number', sa.Integer(), nullable=False),
        sa.Column('error_type', sa.String(), nullable=False),
        sa.Column('message', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(['batch_id'], ['import_batches.id']),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    op.drop_table('import_errors')
    op.drop_index(op.f('ix_inventory_items_book_reference'), table_name='inventory_items')
    op.drop_table('inventory_items')
    op.drop_table('import_batches')
