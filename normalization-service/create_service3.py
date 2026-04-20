import os

# -- test_title_normalizer.py ----------------------------------------------
test_title = """import pytest
from app.domain.normalizers import TitleNormalizer


def test_normalize_title_sentence_case():
    n = TitleNormalizer()
    assert n.normalize("THE GREAT GATSBY") == "The great gatsby"


def test_normalize_title_removes_double_spaces():
    n = TitleNormalizer()
    result = n.normalize("El  senor  de  los  anillos")
    assert "  " not in result


def test_normalize_title_empty():
    n = TitleNormalizer()
    assert n.normalize("") == ""


def test_normalize_title_strips_whitespace():
    n = TitleNormalizer()
    result = n.normalize("  Don Quixote  ")
    assert not result.startswith(" ")
    assert not result.endswith(" ")
"""

# -- test_author_normalizer.py ---------------------------------------------
test_author = """import pytest
from app.domain.normalizers import AuthorNormalizer


def test_normalize_author_first_last():
    n = AuthorNormalizer()
    result = n.normalize("Gabriel Garcia Marquez")
    assert "Marquez" in result
    assert "," in result


def test_normalize_author_already_formatted():
    n = AuthorNormalizer()
    result = n.normalize("Fitzgerald, F. Scott")
    assert "Fitzgerald" in result


def test_normalize_author_removes_accents():
    n = AuthorNormalizer()
    result = n.normalize("Garcia Marquez, Gabriel")
    assert result == "Garcia Marquez, Gabriel"


def test_normalize_author_single_name():
    n = AuthorNormalizer()
    result = n.normalize("Voltaire")
    assert result == "Voltaire"
"""

# -- test_isbn_validator.py ------------------------------------------------
test_isbn = """import pytest
from app.domain.normalizers import ISBNValidator


def test_valid_isbn13():
    v = ISBNValidator()
    assert v.validate("9780743273565") is True


def test_invalid_isbn():
    v = ISBNValidator()
    assert v.validate("123") is False


def test_none_isbn():
    v = ISBNValidator()
    assert v.validate(None) is False


def test_empty_isbn():
    v = ISBNValidator()
    assert v.validate("") is False
"""

# -- test_duplicate_detector.py --------------------------------------------
test_duplicate = """import pytest
from unittest.mock import MagicMock
from app.domain.duplicate_detector import DuplicateDetector


def test_detect_duplicate():
    mock_db = MagicMock()
    mock_db.execute.return_value.fetchone.return_value = ("existing-id",)
    detector = DuplicateDetector(mock_db)
    is_dup, dup_id = detector.detect("9780743273565")
    assert is_dup is True
    assert dup_id == "existing-id"


def test_no_duplicate():
    mock_db = MagicMock()
    mock_db.execute.return_value.fetchone.return_value = None
    detector = DuplicateDetector(mock_db)
    is_dup, dup_id = detector.detect("9780743273565")
    assert is_dup is False
    assert dup_id is None


def test_no_isbn():
    mock_db = MagicMock()
    detector = DuplicateDetector(mock_db)
    is_dup, dup_id = detector.detect(None)
    assert is_dup is False
    assert dup_id is None
"""

# -- alembic.ini -----------------------------------------------------------
alembic_ini = """[alembic]
script_location = alembic
prepend_sys_path = .
sqlalchemy.url = postgresql://bookflow:bookflow123@postgres:5432/normalization_db

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
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

# -- alembic/script.py.mako ------------------------------------------------
alembic_mako = """from alembic import op
import sqlalchemy as sa
\

revision = \
down_revision = \
branch_labels = \
depends_on = \


def upgrade() -> None:
    \


def downgrade() -> None:
    \
"""

# -- alembic/versions/migration --------------------------------------------
migration = """from alembic import op
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
"""

files = {
    'tests/test_title_normalizer.py': test_title,
    'tests/test_author_normalizer.py': test_author,
    'tests/test_isbn_validator.py': test_isbn,
    'tests/test_duplicate_detector.py': test_duplicate,
    'alembic.ini': alembic_ini,
    'alembic/env.py': alembic_env,
    'alembic/script.py.mako': alembic_mako,
    'alembic/versions/a1b2c3d4e5f6_create_normalization_tables.py': migration,
}

for path, content in files.items():
    full = os.path.join(os.getcwd(), path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Created: {path}')

print('Script 3 done!')
