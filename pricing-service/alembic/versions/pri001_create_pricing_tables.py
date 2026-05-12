from alembic import op
import sqlalchemy as sa

revision = 'pri001_create_pricing_tables'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'pricing_decisions',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('book_reference', sa.String(), nullable=False),
        sa.Column('suggested_price', sa.Float(), nullable=False),
        sa.Column('explanation', sa.String(), nullable=False),
        sa.Column('condition_factor', sa.Float(), nullable=False),
        sa.Column('reference_count', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_pricing_decisions_book_reference', 'pricing_decisions', ['book_reference'])

    op.create_table(
        'price_references',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('source', sa.String(), nullable=False),
        sa.Column('external_price', sa.Float(), nullable=False),
        sa.Column('currency', sa.String(), nullable=True),
        sa.Column('observed_at', sa.DateTime(), nullable=True),
        sa.Column('book_reference', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_price_references_book_reference', 'price_references', ['book_reference'])


def downgrade() -> None:
    op.drop_table('pricing_decisions')
    op.drop_table('price_references')
