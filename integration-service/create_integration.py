import os

# -- requirements.txt ------------------------------------------------------
reqs = """fastapi==0.111.0
uvicorn==0.29.0
pydantic[email]==2.7.1
sqlalchemy==2.0.30
alembic==1.13.1
psycopg2-binary==2.9.9
python-dotenv==1.0.1
httpx==0.27.0
openpyxl==3.1.2
pandas==2.2.2
pytest==8.2.0
pytest-mock==3.14.0
pytest-asyncio==0.23.6
"""

# -- .env ------------------------------------------------------------------
env = """DATABASE_URL=postgresql://bookflow:bookflow123@postgres:5432/integration_db
INVENTORY_URL=http://inventory-service:8002
ENRICHMENT_URL=http://ai-enrichment-service:8004
NORMALIZATION_URL=http://normalization-service:8005
CATALOG_URL=http://catalog-service:8003
SERVICE_PORT=8006
FLOW_TIMEOUT_SECONDS=30
"""

env_example = """DATABASE_URL=postgresql://user:password@postgres:5432/integration_db
INVENTORY_URL=http://inventory-service:8002
ENRICHMENT_URL=http://ai-enrichment-service:8004
NORMALIZATION_URL=http://normalization-service:8005
CATALOG_URL=http://catalog-service:8003
SERVICE_PORT=8006
FLOW_TIMEOUT_SECONDS=30
"""

# -- entities.py -----------------------------------------------------------
entities = """from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
from enum import Enum
import uuid


class StepStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class FlowStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    PARTIAL = "partial"
    FAILED = "failed"


@dataclass
class FlowStep:
    step_name: str
    status: StepStatus = StepStatus.PENDING
    error_message: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    def start(self):
        self.status = StepStatus.RUNNING
        self.started_at = datetime.utcnow()

    def complete(self):
        self.status = StepStatus.COMPLETED
        self.completed_at = datetime.utcnow()

    def fail(self, error: str):
        self.status = StepStatus.FAILED
        self.error_message = error
        self.completed_at = datetime.utcnow()


@dataclass
class IntegrationFlow:
    id: str
    batch_id: str
    status: FlowStatus
    steps: List[FlowStep]
    created_at: datetime
    updated_at: datetime
    total_books: int = 0
    processed_books: int = 0
    failed_books: int = 0

    @staticmethod
    def create(batch_id: str) -> 'IntegrationFlow':
        now = datetime.utcnow()
        steps = [
            FlowStep(step_name="inventory"),
            FlowStep(step_name="enrichment"),
            FlowStep(step_name="normalization"),
            FlowStep(step_name="catalog"),
        ]
        return IntegrationFlow(
            id=str(uuid.uuid4()),
            batch_id=batch_id,
            status=FlowStatus.PENDING,
            steps=steps,
            created_at=now,
            updated_at=now,
        )

    def get_step(self, name: str) -> Optional[FlowStep]:
        return next((s for s in self.steps if s.step_name == name), None)

    def update_status(self):
        statuses = [s.status for s in self.steps]
        if all(s == StepStatus.COMPLETED for s in statuses):
            self.status = FlowStatus.COMPLETED
        elif any(s == StepStatus.FAILED for s in statuses):
            completed = sum(1 for s in statuses if s == StepStatus.COMPLETED)
            self.status = FlowStatus.PARTIAL if completed > 0 else FlowStatus.FAILED
        elif any(s == StepStatus.RUNNING for s in statuses):
            self.status = FlowStatus.RUNNING
        self.updated_at = datetime.utcnow()
"""

# -- schemas.py ------------------------------------------------------------
schemas = """from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.domain.entities import StepStatus, FlowStatus


class FlowStepResponse(BaseModel):
    step_name: str
    status: StepStatus
    error_message: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class IntegrationFlowResponse(BaseModel):
    id: str
    batch_id: str
    status: FlowStatus
    steps: List[FlowStepResponse]
    created_at: datetime
    updated_at: datetime
    total_books: int
    processed_books: int
    failed_books: int

    class Config:
        from_attributes = True


class TriggerResponse(BaseModel):
    flow_id: str
    batch_id: str
    status: FlowStatus
    message: str
    steps: List[FlowStepResponse]
"""

# -- repositories.py (domain) ---------------------------------------------
repositories = """from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.entities import IntegrationFlow


class IntegrationFlowRepository(ABC):
    @abstractmethod
    def save(self, flow: IntegrationFlow) -> IntegrationFlow:
        pass

    @abstractmethod
    def find_by_id(self, flow_id: str) -> Optional[IntegrationFlow]:
        pass

    @abstractmethod
    def find_by_batch_id(self, batch_id: str) -> Optional[IntegrationFlow]:
        pass

    @abstractmethod
    def find_all(self) -> List[IntegrationFlow]:
        pass
"""

# -- models.py -------------------------------------------------------------
models = """from sqlalchemy import Column, String, Integer, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class IntegrationFlowModel(Base):
    __tablename__ = "integration_flows"

    id = Column(String, primary_key=True)
    batch_id = Column(String, nullable=False, index=True)
    status = Column(String, nullable=False, default="pending")
    steps = Column(JSON, nullable=False, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    total_books = Column(Integer, default=0)
    processed_books = Column(Integer, default=0)
    failed_books = Column(Integer, default=0)
"""

# -- database.py -----------------------------------------------------------
database = """import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
"""

# -- infrastructure/repositories.py ---------------------------------------
infra_repo = """from typing import Optional, List
from sqlalchemy.orm import Session
from app.domain.entities import IntegrationFlow, FlowStep, StepStatus, FlowStatus
from app.domain.repositories import IntegrationFlowRepository
from app.infrastructure.models import IntegrationFlowModel
from datetime import datetime


class IntegrationFlowRepositoryPostgres(IntegrationFlowRepository):
    def __init__(self, db: Session):
        self.db = db

    def save(self, flow: IntegrationFlow) -> IntegrationFlow:
        steps_data = [
            {
                "step_name": s.step_name,
                "status": s.status.value,
                "error_message": s.error_message,
                "started_at": s.started_at.isoformat() if s.started_at else None,
                "completed_at": s.completed_at.isoformat() if s.completed_at else None,
            }
            for s in flow.steps
        ]
        existing = self.db.query(IntegrationFlowModel).filter(
            IntegrationFlowModel.id == flow.id
        ).first()
        if existing:
            existing.status = flow.status.value
            existing.steps = steps_data
            existing.updated_at = flow.updated_at
            existing.total_books = flow.total_books
            existing.processed_books = flow.processed_books
            existing.failed_books = flow.failed_books
            self.db.commit()
            self.db.refresh(existing)
        else:
            model = IntegrationFlowModel(
                id=flow.id,
                batch_id=flow.batch_id,
                status=flow.status.value,
                steps=steps_data,
                created_at=flow.created_at,
                updated_at=flow.updated_at,
                total_books=flow.total_books,
                processed_books=flow.processed_books,
                failed_books=flow.failed_books,
            )
            self.db.add(model)
            self.db.commit()
            self.db.refresh(model)
        return flow

    def find_by_id(self, flow_id: str) -> Optional[IntegrationFlow]:
        model = self.db.query(IntegrationFlowModel).filter(
            IntegrationFlowModel.id == flow_id
        ).first()
        return self._to_entity(model) if model else None

    def find_by_batch_id(self, batch_id: str) -> Optional[IntegrationFlow]:
        model = self.db.query(IntegrationFlowModel).filter(
            IntegrationFlowModel.batch_id == batch_id
        ).order_by(IntegrationFlowModel.created_at.desc()).first()
        return self._to_entity(model) if model else None

    def find_all(self) -> List[IntegrationFlow]:
        models = self.db.query(IntegrationFlowModel).order_by(
            IntegrationFlowModel.created_at.desc()
        ).all()
        return [self._to_entity(m) for m in models]

    def _to_entity(self, model: IntegrationFlowModel) -> IntegrationFlow:
        steps = []
        for s in model.steps:
            step = FlowStep(step_name=s["step_name"])
            step.status = StepStatus(s["status"])
            step.error_message = s.get("error_message")
            if s.get("started_at"):
                step.started_at = datetime.fromisoformat(s["started_at"])
            if s.get("completed_at"):
                step.completed_at = datetime.fromisoformat(s["completed_at"])
            steps.append(step)
        return IntegrationFlow(
            id=model.id,
            batch_id=model.batch_id,
            status=FlowStatus(model.status),
            steps=steps,
            created_at=model.created_at,
            updated_at=model.updated_at,
            total_books=model.total_books,
            processed_books=model.processed_books,
            failed_books=model.failed_books,
        )
"""

# -- clients.py ------------------------------------------------------------
clients = """import os
import httpx
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

INVENTORY_URL = os.getenv("INVENTORY_URL", "http://inventory-service:8002")
ENRICHMENT_URL = os.getenv("ENRICHMENT_URL", "http://ai-enrichment-service:8004")
NORMALIZATION_URL = os.getenv("NORMALIZATION_URL", "http://normalization-service:8005")
CATALOG_URL = os.getenv("CATALOG_URL", "http://catalog-service:8003")
TIMEOUT = int(os.getenv("FLOW_TIMEOUT_SECONDS", "30"))


class InventoryClient:
    async def get_batch(self, batch_id: str) -> dict:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            r = await client.get(f"{INVENTORY_URL}/inventory/batches/{batch_id}")
            r.raise_for_status()
            return r.json()

    async def get_batch_items(self, batch_id: str) -> list:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            r = await client.get(f"{INVENTORY_URL}/inventory/batches/{batch_id}/summary")
            r.raise_for_status()
            return r.json()


class EnrichmentClient:
    async def enrich(self, book_reference: str, title: str, author: str, isbn: Optional[str] = None) -> dict:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            r = await client.post(f"{ENRICHMENT_URL}/enrichment/enrich", json={
                "book_reference": book_reference,
                "title": title,
                "author": author,
                "isbn": isbn,
            })
            r.raise_for_status()
            return r.json()


class NormalizationClient:
    async def normalize(self, enrichment_result_id: str, title: str, author: str, isbn: Optional[str] = None) -> dict:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            r = await client.post(f"{NORMALIZATION_URL}/normalization/normalize", json={
                "enrichment_result_id": enrichment_result_id,
                "title": title,
                "author": author,
                "isbn": isbn,
            })
            r.raise_for_status()
            return r.json()


class CatalogClient:
    async def get_categories(self) -> list:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            r = await client.get(f"{CATALOG_URL}/catalog/categories")
            r.raise_for_status()
            return r.json()

    async def register_book(self, book_data: dict) -> dict:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            r = await client.post(f"{CATALOG_URL}/catalog/books", json=book_data)
            r.raise_for_status()
            return r.json()
"""

# -- use_cases.py ---------------------------------------------------------
use_cases = """import os
from typing import List
from app.domain.entities import IntegrationFlow, FlowStatus
from app.domain.repositories import IntegrationFlowRepository
from app.infrastructure.clients import (
    InventoryClient, EnrichmentClient, NormalizationClient, CatalogClient
)


class TriggerEnrichmentFlow:
    def __init__(self, repository: IntegrationFlowRepository):
        self.repository = repository
        self.inventory_client = InventoryClient()
        self.enrichment_client = EnrichmentClient()
        self.normalization_client = NormalizationClient()
        self.catalog_client = CatalogClient()

    async def execute(self, batch_id: str) -> IntegrationFlow:
        flow = IntegrationFlow.create(batch_id)
        flow.status = FlowStatus.RUNNING
        self.repository.save(flow)

        # Step 1: Inventory
        inventory_step = flow.get_step("inventory")
        inventory_step.start()
        try:
            batch = await self.inventory_client.get_batch(batch_id)
            flow.total_books = batch.get("valid_rows", 0)
            inventory_step.complete()
        except Exception as e:
            inventory_step.fail(str(e))
            flow.update_status()
            self.repository.save(flow)
            return flow
        self.repository.save(flow)

        # Step 2: Enrichment
        enrichment_step = flow.get_step("enrichment")
        enrichment_step.start()
        enriched_results = []
        try:
            books = [
                {"book_reference": f"REF-{batch_id}-{i}", "title": f"Book {i}", "author": "Unknown"}
                for i in range(min(flow.total_books, 5))
            ]
            for book in books:
                try:
                    result = await self.enrichment_client.enrich(
                        book_reference=book["book_reference"],
                        title=book["title"],
                        author=book["author"],
                    )
                    enriched_results.append(result)
                    flow.processed_books += 1
                except Exception:
                    flow.failed_books += 1
            enrichment_step.complete()
        except Exception as e:
            enrichment_step.fail(str(e))
        self.repository.save(flow)

        # Step 3: Normalization
        normalization_step = flow.get_step("normalization")
        normalization_step.start()
        normalized_results = []
        try:
            for result in enriched_results:
                try:
                    normalized = await self.normalization_client.normalize(
                        enrichment_result_id=result.get("id", "unknown"),
                        title=result.get("normalized_title", "Unknown"),
                        author=result.get("normalized_author", "Unknown"),
                        isbn=result.get("normalized_isbn"),
                    )
                    normalized_results.append(normalized)
                except Exception:
                    pass
            normalization_step.complete()
        except Exception as e:
            normalization_step.fail(str(e))
        self.repository.save(flow)

        # Step 4: Catalog
        catalog_step = flow.get_step("catalog")
        catalog_step.start()
        try:
            categories = await self.catalog_client.get_categories()
            default_category_id = categories[0]["id"] if categories else None
            for normalized in normalized_results:
                try:
                    if default_category_id and not normalized.get("is_duplicate"):
                        await self.catalog_client.register_book({
                            "title": normalized.get("normalized_title", "Unknown"),
                            "author": normalized.get("normalized_author", "Unknown"),
                            "publisher": "BookFlow Import",
                            "category_id": default_category_id,
                            "isbn": normalized.get("normalized_isbn"),
                        })
                except Exception:
                    pass
            catalog_step.complete()
        except Exception as e:
            catalog_step.fail(str(e))
        self.repository.save(flow)

        flow.update_status()
        self.repository.save(flow)
        return flow


class GetFlowStatus:
    def __init__(self, repository: IntegrationFlowRepository):
        self.repository = repository

    def execute(self, batch_id: str):
        return self.repository.find_by_batch_id(batch_id)


class GetAllFlows:
    def __init__(self, repository: IntegrationFlowRepository):
        self.repository = repository

    def execute(self):
        return self.repository.find_all()
"""

# -- integration_router.py -------------------------------------------------
router = """from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.domain.schemas import TriggerResponse, IntegrationFlowResponse, FlowStepResponse
from app.infrastructure.repositories import IntegrationFlowRepositoryPostgres
from app.infrastructure.database import get_db
from app.application.use_cases import TriggerEnrichmentFlow, GetFlowStatus, GetAllFlows
from typing import List

router = APIRouter(prefix="/integration", tags=["integration"])


@router.post("/trigger/{batch_id}", response_model=TriggerResponse, status_code=201)
async def trigger_flow(batch_id: str, db: Session = Depends(get_db)):
    try:
        repository = IntegrationFlowRepositoryPostgres(db)
        use_case = TriggerEnrichmentFlow(repository)
        flow = await use_case.execute(batch_id)
        return TriggerResponse(
            flow_id=flow.id,
            batch_id=flow.batch_id,
            status=flow.status,
            message=f"Flow completed with status: {flow.status.value}",
            steps=[
                FlowStepResponse(
                    step_name=s.step_name,
                    status=s.status,
                    error_message=s.error_message,
                    started_at=s.started_at,
                    completed_at=s.completed_at,
                ) for s in flow.steps
            ]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status/{batch_id}", response_model=IntegrationFlowResponse)
def get_status(batch_id: str, db: Session = Depends(get_db)):
    try:
        repository = IntegrationFlowRepositoryPostgres(db)
        use_case = GetFlowStatus(repository)
        flow = use_case.execute(batch_id)
        if not flow:
            raise HTTPException(status_code=404, detail="Flow not found for this batch_id")
        return IntegrationFlowResponse(
            id=flow.id,
            batch_id=flow.batch_id,
            status=flow.status,
            steps=[
                FlowStepResponse(
                    step_name=s.step_name,
                    status=s.status,
                    error_message=s.error_message,
                    started_at=s.started_at,
                    completed_at=s.completed_at,
                ) for s in flow.steps
            ],
            created_at=flow.created_at,
            updated_at=flow.updated_at,
            total_books=flow.total_books,
            processed_books=flow.processed_books,
            failed_books=flow.failed_books,
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/flows", response_model=List[IntegrationFlowResponse])
def get_all_flows(db: Session = Depends(get_db)):
    try:
        repository = IntegrationFlowRepositoryPostgres(db)
        use_case = GetAllFlows(repository)
        flows = use_case.execute()
        return [
            IntegrationFlowResponse(
                id=f.id,
                batch_id=f.batch_id,
                status=f.status,
                steps=[
                    FlowStepResponse(
                        step_name=s.step_name,
                        status=s.status,
                        error_message=s.error_message,
                        started_at=s.started_at,
                        completed_at=s.completed_at,
                    ) for s in f.steps
                ],
                created_at=f.created_at,
                updated_at=f.updated_at,
                total_books=f.total_books,
                processed_books=f.processed_books,
                failed_books=f.failed_books,
            ) for f in flows
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
def health():
    return {"status": "ok", "service": "integration-service"}
"""

# -- main.py ---------------------------------------------------------------
main = """import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.routers.integration_router import router
from app.infrastructure.database import engine
from app.infrastructure.models import Base

load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Integration Service",
    description="Servicio de integracion y orquestacion del flujo end to end de BookFlow",
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
    return {"status": "ok", "service": "integration-service"}
"""

# -- Dockerfile ------------------------------------------------------------
dockerfile = """FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8006
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8006"]
"""

# -- alembic.ini -----------------------------------------------------------
alembic_ini = """[alembic]
script_location = alembic
prepend_sys_path = .
sqlalchemy.url = postgresql://bookflow:bookflow123@postgres:5432/integration_db

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
    'app/domain/schemas.py': schemas,
    'app/domain/repositories.py': repositories,
    'app/infrastructure/models.py': models,
    'app/infrastructure/database.py': database,
    'app/infrastructure/repositories.py': infra_repo,
    'app/infrastructure/clients.py': clients,
    'app/application/use_cases.py': use_cases,
    'app/routers/integration_router.py': router,
    'main.py': main,
    'Dockerfile': dockerfile,
    'alembic.ini': alembic_ini,
}

for path, content in files.items():
    full = os.path.join(os.getcwd(), path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Created: {path}')

print('Integration service files done!')
