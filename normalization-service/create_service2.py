import os

# -- models.py -------------------------------------------------------------
models = """from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class NormalizedRecordModel(Base):
    __tablename__ = "normalized_records"

    id = Column(String, primary_key=True)
    enrichment_result_id = Column(String, nullable=False)
    normalized_title = Column(String, nullable=False)
    normalized_author = Column(String, nullable=False)
    normalized_isbn = Column(String, nullable=True)
    isbn_valid = Column(Boolean, default=True)
    issn_valid = Column(Boolean, default=True)
    is_duplicate = Column(Boolean, default=False)
    duplicate_of_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
"""

# -- database.py -----------------------------------------------------------
database = """import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
CATALOG_DB_URL = os.getenv("CATALOG_DB_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

catalog_engine = create_engine(CATALOG_DB_URL)
CatalogSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=catalog_engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_catalog_db():
    db = CatalogSessionLocal()
    try:
        yield db
    finally:
        db.close()
"""

# -- infrastructure/repositories.py ---------------------------------------
infra_repo = """from typing import List, Optional
from sqlalchemy.orm import Session
from app.domain.entities import NormalizedRecord
from app.domain.repositories import NormalizedRecordRepository
from app.infrastructure.models import NormalizedRecordModel
from datetime import datetime


class NormalizedRecordRepositoryPostgres(NormalizedRecordRepository):
    def __init__(self, db: Session):
        self.db = db

    def save(self, record: NormalizedRecord) -> NormalizedRecord:
        model = NormalizedRecordModel(
            id=record.id,
            enrichment_result_id=record.enrichment_result_id,
            normalized_title=record.normalized_title,
            normalized_author=record.normalized_author,
            normalized_isbn=record.normalized_isbn,
            isbn_valid=record.isbn_valid,
            issn_valid=record.issn_valid,
            is_duplicate=record.is_duplicate,
            duplicate_of_id=record.duplicate_of_id,
            created_at=record.created_at,
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return record

    def find_all(self) -> List[NormalizedRecord]:
        models = self.db.query(NormalizedRecordModel).all()
        return [self._to_entity(m) for m in models]

    def find_by_id(self, record_id: str) -> Optional[NormalizedRecord]:
        model = self.db.query(NormalizedRecordModel).filter(
            NormalizedRecordModel.id == record_id
        ).first()
        return self._to_entity(model) if model else None

    def _to_entity(self, model: NormalizedRecordModel) -> NormalizedRecord:
        return NormalizedRecord(
            id=model.id,
            enrichment_result_id=model.enrichment_result_id,
            normalized_title=model.normalized_title,
            normalized_author=model.normalized_author,
            normalized_isbn=model.normalized_isbn,
            isbn_valid=model.isbn_valid,
            issn_valid=model.issn_valid,
            is_duplicate=model.is_duplicate,
            duplicate_of_id=model.duplicate_of_id,
            created_at=model.created_at,
        )
"""

# -- use_cases.py ----------------------------------------------------------
use_cases = """from typing import List
from app.domain.entities import NormalizedRecord
from app.domain.normalizers import TitleNormalizer, AuthorNormalizer, ISBNValidator, ISSNValidator
from app.domain.duplicate_detector import DuplicateDetector
from app.domain.repositories import NormalizedRecordRepository
from app.domain.schemas import EnrichmentResultInput


class NormalizationPipeline:
    def __init__(self):
        self.title_normalizer = TitleNormalizer()
        self.author_normalizer = AuthorNormalizer()
        self.isbn_validator = ISBNValidator()
        self.issn_validator = ISSNValidator()

    def run(self, input_data: EnrichmentResultInput, duplicate_detector: DuplicateDetector) -> NormalizedRecord:
        normalized_title = self.title_normalizer.normalize(input_data.title)
        normalized_author = self.author_normalizer.normalize(input_data.author)
        isbn_valid = self.isbn_validator.validate(input_data.isbn)
        issn_valid = self.issn_validator.validate(input_data.issn)
        is_duplicate, duplicate_of_id = duplicate_detector.detect(input_data.isbn)

        return NormalizedRecord.create(
            enrichment_result_id=input_data.enrichment_result_id,
            normalized_title=normalized_title,
            normalized_author=normalized_author,
            normalized_isbn=input_data.isbn,
            isbn_valid=isbn_valid,
            issn_valid=issn_valid,
            is_duplicate=is_duplicate,
            duplicate_of_id=duplicate_of_id,
        )


class NormalizeRecord:
    def __init__(self, repository: NormalizedRecordRepository, duplicate_detector: DuplicateDetector):
        self.repository = repository
        self.duplicate_detector = duplicate_detector
        self.pipeline = NormalizationPipeline()

    def execute(self, input_data: EnrichmentResultInput) -> NormalizedRecord:
        record = self.pipeline.run(input_data, self.duplicate_detector)
        return self.repository.save(record)


class NormalizeBatch:
    def __init__(self, repository: NormalizedRecordRepository, duplicate_detector: DuplicateDetector):
        self.repository = repository
        self.duplicate_detector = duplicate_detector
        self.pipeline = NormalizationPipeline()

    def execute(self, inputs: List[EnrichmentResultInput]) -> List[NormalizedRecord]:
        results = []
        for input_data in inputs:
            record = self.pipeline.run(input_data, self.duplicate_detector)
            saved = self.repository.save(record)
            results.append(saved)
        return results


class GetRecords:
    def __init__(self, repository: NormalizedRecordRepository):
        self.repository = repository

    def execute(self) -> List[NormalizedRecord]:
        return self.repository.find_all()
"""

# -- normalization_router.py -----------------------------------------------
router = """from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.domain.schemas import EnrichmentResultInput, NormalizedRecordResponse, BatchInput, BatchResponse
from app.infrastructure.repositories import NormalizedRecordRepositoryPostgres
from app.infrastructure.database import get_db, get_catalog_db
from app.domain.duplicate_detector import DuplicateDetector
from app.application.use_cases import NormalizeRecord, NormalizeBatch, GetRecords

router = APIRouter(prefix="/normalization", tags=["normalization"])


@router.post("/normalize", response_model=NormalizedRecordResponse, status_code=201)
def normalize_record(
    input_data: EnrichmentResultInput,
    db: Session = Depends(get_db),
    catalog_db: Session = Depends(get_catalog_db),
):
    try:
        repository = NormalizedRecordRepositoryPostgres(db)
        detector = DuplicateDetector(catalog_db)
        use_case = NormalizeRecord(repository, detector)
        record = use_case.execute(input_data)
        return NormalizedRecordResponse(
            id=record.id,
            enrichment_result_id=record.enrichment_result_id,
            normalized_title=record.normalized_title,
            normalized_author=record.normalized_author,
            normalized_isbn=record.normalized_isbn,
            isbn_valid=record.isbn_valid,
            issn_valid=record.issn_valid,
            is_duplicate=record.is_duplicate,
            duplicate_of_id=record.duplicate_of_id,
            created_at=record.created_at,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/batch", response_model=BatchResponse, status_code=201)
def normalize_batch(
    batch: BatchInput,
    db: Session = Depends(get_db),
    catalog_db: Session = Depends(get_catalog_db),
):
    try:
        repository = NormalizedRecordRepositoryPostgres(db)
        detector = DuplicateDetector(catalog_db)
        use_case = NormalizeBatch(repository, detector)
        records = use_case.execute(batch.records)
        return BatchResponse(
            processed=len(records),
            results=[
                NormalizedRecordResponse(
                    id=r.id,
                    enrichment_result_id=r.enrichment_result_id,
                    normalized_title=r.normalized_title,
                    normalized_author=r.normalized_author,
                    normalized_isbn=r.normalized_isbn,
                    isbn_valid=r.isbn_valid,
                    issn_valid=r.issn_valid,
                    is_duplicate=r.is_duplicate,
                    duplicate_of_id=r.duplicate_of_id,
                    created_at=r.created_at,
                ) for r in records
            ]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/records", response_model=List[NormalizedRecordResponse])
def get_records(
    db: Session = Depends(get_db),
    catalog_db: Session = Depends(get_catalog_db),
):
    try:
        repository = NormalizedRecordRepositoryPostgres(db)
        detector = DuplicateDetector(catalog_db)
        use_case = GetRecords(repository)
        records = use_case.execute()
        return [
            NormalizedRecordResponse(
                id=r.id,
                enrichment_result_id=r.enrichment_result_id,
                normalized_title=r.normalized_title,
                normalized_author=r.normalized_author,
                normalized_isbn=r.normalized_isbn,
                isbn_valid=r.isbn_valid,
                issn_valid=r.issn_valid,
                is_duplicate=r.is_duplicate,
                duplicate_of_id=r.duplicate_of_id,
                created_at=r.created_at,
            ) for r in records
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
def health():
    return {"status": "ok", "service": "normalization-service"}
"""

# -- main.py ---------------------------------------------------------------
main = """import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.routers.normalization_router import router
from app.infrastructure.database import engine
from app.infrastructure.models import Base

load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Normalization Service",
    description="Servicio de limpieza y normalizacion de datos bibliograficos",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/health")
def health():
    return {"status": "ok", "service": "normalization-service"}
"""

# -- Dockerfile ------------------------------------------------------------
dockerfile = """FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8005
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8005"]
"""

files = {
    'app/infrastructure/models.py': models,
    'app/infrastructure/database.py': database,
    'app/infrastructure/repositories.py': infra_repo,
    'app/application/use_cases.py': use_cases,
    'app/routers/normalization_router.py': router,
    'main.py': main,
    'Dockerfile': dockerfile,
}

for path, content in files.items():
    full = os.path.join(os.getcwd(), path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Created: {path}')

print('Script 2 done!')
