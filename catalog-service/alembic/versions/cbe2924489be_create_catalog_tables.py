from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = 'cbe2924489be'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'categories',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
    )
    op.create_table(
        'books',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('author', sa.String(), nullable=False),
        sa.Column('publisher', sa.String(), nullable=False),
        sa.Column('category_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('isbn', sa.String(), nullable=True),
        sa.Column('issn', sa.String(), nullable=True),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('cover_url', sa.String(), nullable=True),
        sa.Column('publication_year', sa.Integer(), nullable=True),
        sa.Column('volume', sa.String(), nullable=True),
        sa.Column('enriched_flag', sa.Boolean(), nullable=True),
        sa.Column('published_flag', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['category_id'], ['categories.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('isbn'),
    )
    op.create_index(op.f('ix_books_title'), 'books', ['title'])
    op.create_index(op.f('ix_books_author'), 'books', ['author'])


def downgrade() -> None:
    op.drop_index(op.f('ix_books_author'), table_name='books')
    op.drop_index(op.f('ix_books_title'), table_name='books')
    op.drop_table('books')
    op.drop_table('categories')
