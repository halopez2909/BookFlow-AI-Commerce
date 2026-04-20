from alembic import op
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
