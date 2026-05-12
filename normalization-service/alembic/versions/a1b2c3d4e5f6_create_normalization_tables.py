from alembic import op
import sqlalchemy as sa

revision = 'a1b2c3d4e5f6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'normalized_records',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('enrichment_result_id', sa.String(), nullable=False),
        sa.Column('normalized_title', sa.String(), nullable=False),
        sa.Column('normalized_author', sa.String(), nullable=False),
        sa.Column('normalized_isbn', sa.String(), nullable=True),
        sa.Column('isbn_valid', sa.Boolean(), nullable=True),
        sa.Column('issn_valid', sa.Boolean(), nullable=True),
        sa.Column('is_duplicate', sa.Boolean(), nullable=True),
        sa.Column('duplicate_of_id', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('normalized_records')
