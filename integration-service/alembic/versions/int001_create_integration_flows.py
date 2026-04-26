from alembic import op
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
