import os

# -- requirements.txt ------------------------------------------------------
reqs = """fastapi==0.111.0
uvicorn==0.29.0
pydantic[email]==2.7.1
sqlalchemy==2.0.30
alembic==1.13.1
psycopg2-binary==2.9.9
python-dotenv==1.0.1
unidecode==1.3.8
stdnum==1.20
httpx==0.27.0
pytest==8.2.0
pytest-mock==3.14.0
"""

# -- .env ------------------------------------------------------------------
env = """DATABASE_URL=postgresql://bookflow:bookflow123@postgres:5432/normalization_db
ENRICHMENT_DB_URL=postgresql://bookflow:bookflow123@postgres:5432/enrichment_db
CATALOG_DB_URL=postgresql://bookflow:bookflow123@postgres:5432/catalog_db
SERVICE_PORT=8005
"""

# -- .env.example ----------------------------------------------------------
env_example = """DATABASE_URL=postgresql://user:password@postgres:5432/normalization_db
ENRICHMENT_DB_URL=postgresql://user:password@postgres:5432/enrichment_db
CATALOG_DB_URL=postgresql://user:password@postgres:5432/catalog_db
SERVICE_PORT=8005
"""

# -- entities.py -----------------------------------------------------------
entities = """from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import uuid


@dataclass(frozen=True)
class NormalizedRecord:
    id: str
    enrichment_result_id: str
    normalized_title: str
    normalized_author: str
    normalized_isbn: Optional[str]
    isbn_valid: bool
    issn_valid: bool
    is_duplicate: bool
    duplicate_of_id: Optional[str]
    created_at: datetime

    @staticmethod
    def create(
        enrichment_result_id: str,
        normalized_title: str,
        normalized_author: str,
        normalized_isbn: Optional[str] = None,
        isbn_valid: bool = True,
        issn_valid: bool = True,
        is_duplicate: bool = False,
        duplicate_of_id: Optional[str] = None,
    ) -> 'NormalizedRecord':
        return NormalizedRecord(
            id=str(uuid.uuid4()),
            enrichment_result_id=enrichment_result_id,
            normalized_title=normalized_title,
            normalized_author=normalized_author,
            normalized_isbn=normalized_isbn,
            isbn_valid=isbn_valid,
            issn_valid=issn_valid,
            is_duplicate=is_duplicate,
            duplicate_of_id=duplicate_of_id,
            created_at=datetime.utcnow(),
        )
"""

# -- normalizers.py --------------------------------------------------------
normalizers = """import re
from abc import ABC, abstractmethod
from typing import Optional
from unidecode import unidecode


class Normalizer(ABC):
    @abstractmethod
    def normalize(self, value: str) -> str:
        pass


class TitleNormalizer(Normalizer):
    def normalize(self, value: str) -> str:
        if not value:
            return value
        cleaned = re.sub(r'\\s+', ' ', value.strip())
        cleaned = re.sub(r'[^\\w\\s\\-\\'\\:\\,\\.\\(\\)\\!\\?]', '', cleaned)
        return cleaned[0].upper() + cleaned[1:].lower() if cleaned else cleaned


class AuthorNormalizer(Normalizer):
    def normalize(self, value: str) -> str:
        if not value:
            return value
        normalized = unidecode(value.strip())
        parts = normalized.split(',')
        if len(parts) == 2:
            return f"{parts[0].strip()}, {parts[1].strip()}"
        parts = normalized.split()
        if len(parts) >= 2:
            last = parts[-1]
            first = ' '.join(parts[:-1])
            return f"{last}, {first}"
        return normalized


class ISBNValidator:
    def validate(self, isbn: Optional[str]) -> bool:
        if not isbn:
            return False
        try:
            from stdnum import isbn as isbn_lib
            return isbn_lib.is_valid(isbn)
        except Exception:
            return False


class ISSNValidator:
    def validate(self, issn: Optional[str]) -> bool:
        if not issn:
            return True
        try:
            from stdnum import issn as issn_lib
            return issn_lib.is_valid(issn)
        except Exception:
            return False
"""

# -- duplicate_detector.py -------------------------------------------------
duplicate_detector = """from typing import Optional, Tuple
from sqlalchemy.orm import Session


class DuplicateDetector:
    def __init__(self, catalog_db: Session):
        self.catalog_db = catalog_db

    def detect(self, isbn: Optional[str]) -> Tuple[bool, Optional[str]]:
        if not isbn:
            return False, None
        try:
            from sqlalchemy import text
            result = self.catalog_db.execute(
                text("SELECT id FROM books WHERE isbn = :isbn LIMIT 1"),
                {"isbn": isbn}
            ).fetchone()
            if result:
                return True, str(result[0])
            return False, None
        except Exception:
            return False, None
"""

# -- repositories.py (domain) ----------------------------------------------
repositories = """from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities import NormalizedRecord


class NormalizedRecordRepository(ABC):
    @abstractmethod
    def save(self, record: NormalizedRecord) -> NormalizedRecord:
        pass

    @abstractmethod
    def find_all(self) -> List[NormalizedRecord]:
        pass

    @abstractmethod
    def find_by_id(self, record_id: str) -> Optional[NormalizedRecord]:
        pass
"""

# -- schemas.py ------------------------------------------------------------
schemas = """from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class EnrichmentResultInput(BaseModel):
    enrichment_result_id: str
    title: str
    author: str
    isbn: Optional[str] = None
    issn: Optional[str] = None


class NormalizedRecordResponse(BaseModel):
    id: str
    enrichment_result_id: str
    normalized_title: str
    normalized_author: str
    normalized_isbn: Optional[str] = None
    isbn_valid: bool
    issn_valid: bool
    is_duplicate: bool
    duplicate_of_id: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class BatchInput(BaseModel):
    records: List[EnrichmentResultInput]


class BatchResponse(BaseModel):
    processed: int
    results: List[NormalizedRecordResponse]
"""

files = {
    'requirements.txt': reqs,
    '.env': env,
    '.env.example': env_example,
    'app/__init__.py': '',
    'app/domain/__init__.py': '',
    'app/application/__init__.py': '',
    'app/infrastructure/__init__.py': '',
    'app/routers/__init__.py': '',
    'tests/__init__.py': '',
    'app/domain/entities.py': entities,
    'app/domain/normalizers.py': normalizers,
    'app/domain/duplicate_detector.py': duplicate_detector,
    'app/domain/repositories.py': repositories,
    'app/domain/schemas.py': schemas,
}

for path, content in files.items():
    full = os.path.join(os.getcwd(), path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Created: {path}')

print('Script 1 done!')
