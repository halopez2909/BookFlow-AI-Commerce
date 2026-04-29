import os

reqs = """fastapi==0.111.0
uvicorn==0.29.0
pydantic[email]==2.7.1
sqlalchemy==2.0.30
alembic==1.13.1
psycopg2-binary==2.9.9
python-dotenv==1.0.1
httpx==0.27.0
tenacity==8.2.3
cachetools==5.3.3
pytest==8.2.0
pytest-mock==3.14.0
"""

env = """DATABASE_URL=postgresql://bookflow:bookflow123@postgres:5432/pricing_db
EBAY_APP_ID=
BASE_PRICE_NEW=45000
BASE_PRICE_GOOD=30000
BASE_PRICE_WORN=15000
BASE_PRICE_DAMAGED=8000
SERVICE_PORT=8008
"""

env_example = """DATABASE_URL=postgresql://user:password@postgres:5432/pricing_db
EBAY_APP_ID=your_ebay_app_id
BASE_PRICE_NEW=45000
BASE_PRICE_GOOD=30000
BASE_PRICE_WORN=15000
BASE_PRICE_DAMAGED=8000
SERVICE_PORT=8008
"""

entities = """from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import uuid


@dataclass(frozen=True)
class PriceReference:
    id: str
    source: str
    external_price: float
    currency: str
    observed_at: datetime
    book_reference: str

    @staticmethod
    def create(source: str, external_price: float, book_reference: str, currency: str = "COP") -> "PriceReference":
        return PriceReference(
            id=str(uuid.uuid4()),
            source=source,
            external_price=external_price,
            currency=currency,
            observed_at=datetime.utcnow(),
            book_reference=book_reference,
        )


@dataclass(frozen=True)
class PricingDecision:
    id: str
    book_reference: str
    suggested_price: float
    explanation: str
    condition_factor: float
    reference_count: int
    created_at: datetime

    @staticmethod
    def create(
        book_reference: str,
        suggested_price: float,
        explanation: str,
        condition_factor: float,
        reference_count: int,
    ) -> "PricingDecision":
        return PricingDecision(
            id=str(uuid.uuid4()),
            book_reference=book_reference,
            suggested_price=suggested_price,
            explanation=explanation,
            condition_factor=condition_factor,
            reference_count=reference_count,
            created_at=datetime.utcnow(),
        )
"""

rules = """import os
from enum import Enum
from typing import Optional


class BookCondition(str, Enum):
    NEW = "new"
    GOOD = "good"
    WORN = "worn"
    DAMAGED = "damaged"


CONDITION_FACTORS = {
    BookCondition.NEW: 1.0,
    BookCondition.GOOD: 0.70,
    BookCondition.WORN: 0.40,
    BookCondition.DAMAGED: 0.20,
}

BASE_PRICES = {
    BookCondition.NEW: float(os.getenv("BASE_PRICE_NEW", "45000")),
    BookCondition.GOOD: float(os.getenv("BASE_PRICE_GOOD", "30000")),
    BookCondition.WORN: float(os.getenv("BASE_PRICE_WORN", "15000")),
    BookCondition.DAMAGED: float(os.getenv("BASE_PRICE_DAMAGED", "8000")),
}

CATEGORY_MULTIPLIERS = {
    "textbook": 1.3,
    "technical": 1.2,
    "fiction": 0.9,
    "children": 0.8,
    "default": 1.0,
}


class ConditionPricingRule:
    def apply(self, condition: str, base_price: Optional[float] = None) -> tuple[float, float, str]:
        try:
            cond = BookCondition(condition.lower())
        except ValueError:
            cond = BookCondition.GOOD

        factor = CONDITION_FACTORS[cond]
        price = base_price or BASE_PRICES[cond]
        final = round(price * factor, -2)

        explanations = {
            BookCondition.NEW: f"Libro nuevo. Factor: {factor}. Precio base:  COP.",
            BookCondition.GOOD: f"Buen estado. Factor de descuento: {factor} ({int((1-factor)*100)}% menos). Base:  COP.",
            BookCondition.WORN: f"Estado desgastado. Factor: {factor} ({int((1-factor)*100)}% descuento). Base:  COP.",
            BookCondition.DAMAGED: f"Libro daniado. Factor minimo: {factor} ({int((1-factor)*100)}% descuento). Base:  COP.",
        }

        return final, factor, explanations[cond]


class CategoryPricingRule:
    def apply(self, suggested_price: float, category: Optional[str]) -> tuple[float, str]:
        if not category:
            return suggested_price, ""
        mult = CATEGORY_MULTIPLIERS.get(category.lower(), CATEGORY_MULTIPLIERS["default"])
        if mult == 1.0:
            return suggested_price, ""
        adjusted = round(suggested_price * mult, -2)
        return adjusted, f" Ajuste por categoria '{category}': x{mult}."
"""

repositories = """from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities import PricingDecision, PriceReference


class PricingDecisionRepository(ABC):
    @abstractmethod
    def save(self, decision: PricingDecision) -> PricingDecision:
        pass

    @abstractmethod
    def find_by_book_reference(self, book_reference: str) -> Optional[PricingDecision]:
        pass

    @abstractmethod
    def find_all(self) -> List[PricingDecision]:
        pass


class PriceReferenceRepository(ABC):
    @abstractmethod
    def save(self, reference: PriceReference) -> PriceReference:
        pass

    @abstractmethod
    def find_by_book_reference(self, book_reference: str) -> List[PriceReference]:
        pass
"""

schemas = """from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PricingRequest(BaseModel):
    book_reference: str
    isbn: Optional[str] = None
    condition: str = "good"
    category: Optional[str] = None
    title: Optional[str] = None


class PricingDecisionResponse(BaseModel):
    id: str
    book_reference: str
    suggested_price: float
    explanation: str
    condition_factor: float
    reference_count: int
    created_at: datetime

    class Config:
        from_attributes = True


class PriceReferenceResponse(BaseModel):
    id: str
    source: str
    external_price: float
    currency: str
    observed_at: datetime
    book_reference: str

    class Config:
        from_attributes = True
"""

models = """from sqlalchemy import Column, String, Float, Integer, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()


class PricingDecisionModel(Base):
    __tablename__ = "pricing_decisions"
    id = Column(String, primary_key=True)
    book_reference = Column(String, nullable=False, index=True)
    suggested_price = Column(Float, nullable=False)
    explanation = Column(String, nullable=False)
    condition_factor = Column(Float, nullable=False)
    reference_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)


class PriceReferenceModel(Base):
    __tablename__ = "price_references"
    id = Column(String, primary_key=True)
    source = Column(String, nullable=False)
    external_price = Column(Float, nullable=False)
    currency = Column(String, default="COP")
    observed_at = Column(DateTime, default=datetime.utcnow)
    book_reference = Column(String, nullable=False, index=True)
"""

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

infra_repo = """from typing import List, Optional
from sqlalchemy.orm import Session
from app.domain.entities import PricingDecision, PriceReference
from app.domain.repositories import PricingDecisionRepository, PriceReferenceRepository
from app.infrastructure.models import PricingDecisionModel, PriceReferenceModel
from datetime import datetime


class PricingDecisionRepositoryPostgres(PricingDecisionRepository):
    def __init__(self, db: Session):
        self.db = db

    def save(self, decision: PricingDecision) -> PricingDecision:
        existing = self.db.query(PricingDecisionModel).filter(
            PricingDecisionModel.book_reference == decision.book_reference
        ).first()
        if existing:
            existing.suggested_price = decision.suggested_price
            existing.explanation = decision.explanation
            existing.condition_factor = decision.condition_factor
            existing.reference_count = decision.reference_count
            existing.created_at = decision.created_at
            self.db.commit()
        else:
            model = PricingDecisionModel(
                id=decision.id,
                book_reference=decision.book_reference,
                suggested_price=decision.suggested_price,
                explanation=decision.explanation,
                condition_factor=decision.condition_factor,
                reference_count=decision.reference_count,
                created_at=decision.created_at,
            )
            self.db.add(model)
            self.db.commit()
        return decision

    def find_by_book_reference(self, book_reference: str) -> Optional[PricingDecision]:
        model = self.db.query(PricingDecisionModel).filter(
            PricingDecisionModel.book_reference == book_reference
        ).order_by(PricingDecisionModel.created_at.desc()).first()
        if not model:
            return None
        return PricingDecision(
            id=model.id, book_reference=model.book_reference,
            suggested_price=model.suggested_price, explanation=model.explanation,
            condition_factor=model.condition_factor, reference_count=model.reference_count,
            created_at=model.created_at,
        )

    def find_all(self) -> List[PricingDecision]:
        models = self.db.query(PricingDecisionModel).order_by(
            PricingDecisionModel.created_at.desc()
        ).all()
        return [PricingDecision(
            id=m.id, book_reference=m.book_reference,
            suggested_price=m.suggested_price, explanation=m.explanation,
            condition_factor=m.condition_factor, reference_count=m.reference_count,
            created_at=m.created_at,
        ) for m in models]


class PriceReferenceRepositoryPostgres(PriceReferenceRepository):
    def __init__(self, db: Session):
        self.db = db

    def save(self, reference: PriceReference) -> PriceReference:
        model = PriceReferenceModel(
            id=reference.id, source=reference.source,
            external_price=reference.external_price, currency=reference.currency,
            observed_at=reference.observed_at, book_reference=reference.book_reference,
        )
        self.db.add(model)
        self.db.commit()
        return reference

    def find_by_book_reference(self, book_reference: str) -> List[PriceReference]:
        models = self.db.query(PriceReferenceModel).filter(
            PriceReferenceModel.book_reference == book_reference
        ).all()
        return [PriceReference(
            id=m.id, source=m.source, external_price=m.external_price,
            currency=m.currency, observed_at=m.observed_at, book_reference=m.book_reference,
        ) for m in models]
"""

ebay_client = """import os
import httpx
from typing import Optional
from cachetools import TTLCache
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from dotenv import load_dotenv

load_dotenv()

EBAY_APP_ID = os.getenv("EBAY_APP_ID", "")
TIMEOUT = int(os.getenv("ENRICHMENT_TIMEOUT_SECONDS", "10"))

_cache = TTLCache(maxsize=256, ttl=3600)


class EbayPriceClient:
    async def get_reference_price(self, isbn: Optional[str], title: Optional[str]) -> Optional[float]:
        if not EBAY_APP_ID or not isbn:
            return None
        cache_key = f"ebay:{isbn}"
        if cache_key in _cache:
            return _cache[cache_key]
        try:
            price = await self._fetch_ebay(isbn, title)
            if price:
                _cache[cache_key] = price
            return price
        except Exception:
            return None

    @retry(
        stop=stop_after_attempt(2),
        wait=wait_exponential(multiplier=1, min=1, max=4),
        retry=retry_if_exception_type(httpx.RequestError),
        reraise=False,
    )
    async def _fetch_ebay(self, isbn: str, title: Optional[str]) -> Optional[float]:
        query = isbn or title or ""
        url = "https://api.ebay.com/buy/browse/v1/item_summary/search"
        headers = {"Authorization": f"Bearer {EBAY_APP_ID}"}
        params = {"q": f"book {query}", "limit": 5, "category_ids": "267"}
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            r = await client.get(url, headers=headers, params=params)
            r.raise_for_status()
            data = r.json()
            items = data.get("itemSummaries", [])
            if not items:
                return None
            prices = []
            for item in items:
                try:
                    p = float(item["price"]["value"])
                    prices.append(p * 4200)
                except Exception:
                    continue
            return round(sum(prices) / len(prices), -2) if prices else None
"""

use_cases = """from typing import Optional
from app.domain.entities import PricingDecision, PriceReference
from app.domain.repositories import PricingDecisionRepository, PriceReferenceRepository
from app.domain.rules import ConditionPricingRule, CategoryPricingRule
from app.infrastructure.ebay_client import EbayPriceClient


class CalculatePrice:
    def __init__(
        self,
        decision_repo: PricingDecisionRepository,
        reference_repo: PriceReferenceRepository,
    ):
        self.decision_repo = decision_repo
        self.reference_repo = reference_repo
        self.condition_rule = ConditionPricingRule()
        self.category_rule = CategoryPricingRule()
        self.ebay_client = EbayPriceClient()

    async def execute(
        self,
        book_reference: str,
        isbn: Optional[str] = None,
        condition: str = "good",
        category: Optional[str] = None,
        title: Optional[str] = None,
    ) -> PricingDecision:
        ebay_price = await self.ebay_client.get_reference_price(isbn, title)

        ref_count = 0
        if ebay_price:
            ref = PriceReference.create(
                source="ebay", external_price=ebay_price, book_reference=book_reference
            )
            self.reference_repo.save(ref)
            ref_count = 1

        suggested, factor, explanation = self.condition_rule.apply(condition, ebay_price)
        cat_adjusted, cat_note = self.category_rule.apply(suggested, category)
        final_price = cat_adjusted
        full_explanation = explanation + cat_note

        if ebay_price:
            full_explanation += f" Referencia eBay:  COP."
        else:
            full_explanation += " Sin referencia externa disponible. Precio basado en reglas internas."

        decision = PricingDecision.create(
            book_reference=book_reference,
            suggested_price=final_price,
            explanation=full_explanation,
            condition_factor=factor,
            reference_count=ref_count,
        )
        return self.decision_repo.save(decision)


class GetPricingDecision:
    def __init__(self, repo: PricingDecisionRepository):
        self.repo = repo

    def execute(self, book_reference: str) -> Optional[PricingDecision]:
        return self.repo.find_by_book_reference(book_reference)


class GetAllDecisions:
    def __init__(self, repo: PricingDecisionRepository):
        self.repo = repo

    def execute(self):
        return self.repo.find_all()
"""

router = """from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.domain.schemas import PricingRequest, PricingDecisionResponse
from app.infrastructure.repositories import PricingDecisionRepositoryPostgres, PriceReferenceRepositoryPostgres
from app.infrastructure.database import get_db
from app.application.use_cases import CalculatePrice, GetPricingDecision, GetAllDecisions
from typing import List

router = APIRouter(prefix="/pricing", tags=["pricing"])


@router.post("/calculate", response_model=PricingDecisionResponse, status_code=201)
async def calculate_price(request: PricingRequest, db: Session = Depends(get_db)):
    try:
        decision_repo = PricingDecisionRepositoryPostgres(db)
        reference_repo = PriceReferenceRepositoryPostgres(db)
        use_case = CalculatePrice(decision_repo, reference_repo)
        decision = await use_case.execute(
            book_reference=request.book_reference,
            isbn=request.isbn,
            condition=request.condition,
            category=request.category,
            title=request.title,
        )
        return PricingDecisionResponse(
            id=decision.id, book_reference=decision.book_reference,
            suggested_price=decision.suggested_price, explanation=decision.explanation,
            condition_factor=decision.condition_factor, reference_count=decision.reference_count,
            created_at=decision.created_at,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/decisions/{book_reference}", response_model=PricingDecisionResponse)
def get_decision(book_reference: str, db: Session = Depends(get_db)):
    try:
        repo = PricingDecisionRepositoryPostgres(db)
        use_case = GetPricingDecision(repo)
        decision = use_case.execute(book_reference)
        if not decision:
            raise HTTPException(status_code=404, detail="No pricing decision found")
        return PricingDecisionResponse(
            id=decision.id, book_reference=decision.book_reference,
            suggested_price=decision.suggested_price, explanation=decision.explanation,
            condition_factor=decision.condition_factor, reference_count=decision.reference_count,
            created_at=decision.created_at,
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/decisions", response_model=List[PricingDecisionResponse])
def get_all_decisions(db: Session = Depends(get_db)):
    try:
        repo = PricingDecisionRepositoryPostgres(db)
        use_case = GetAllDecisions(repo)
        decisions = use_case.execute()
        return [PricingDecisionResponse(
            id=d.id, book_reference=d.book_reference,
            suggested_price=d.suggested_price, explanation=d.explanation,
            condition_factor=d.condition_factor, reference_count=d.reference_count,
            created_at=d.created_at,
        ) for d in decisions]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
def health():
    return {"status": "ok", "service": "pricing-service"}
"""

main = """import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.routers.pricing_router import router
from app.infrastructure.database import engine
from app.infrastructure.models import Base

load_dotenv()
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Pricing Service",
    description="Motor de pricing con IA y reglas de negocio para BookFlow",
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
    return {"status": "ok", "service": "pricing-service"}
"""

dockerfile = """FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8008
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8008"]
"""

test_pricing = """import pytest
from app.domain.rules import ConditionPricingRule, CategoryPricingRule
from app.domain.entities import PricingDecision, PriceReference


def test_condition_rule_new():
    rule = ConditionPricingRule()
    price, factor, explanation = rule.apply("new")
    assert factor == 1.0
    assert price > 0
    assert "nuevo" in explanation.lower() or "new" in explanation.lower()


def test_condition_rule_good():
    rule = ConditionPricingRule()
    price, factor, explanation = rule.apply("good")
    assert factor == 0.70
    assert price > 0


def test_condition_rule_worn():
    rule = ConditionPricingRule()
    price, factor, explanation = rule.apply("worn")
    assert factor == 0.40


def test_condition_rule_damaged():
    rule = ConditionPricingRule()
    price, factor, explanation = rule.apply("damaged")
    assert factor == 0.20


def test_condition_rule_unknown_defaults_good():
    rule = ConditionPricingRule()
    price, factor, explanation = rule.apply("unknown_condition")
    assert factor == 0.70


def test_category_rule_textbook():
    rule = CategoryPricingRule()
    adjusted, note = rule.apply(30000, "textbook")
    assert adjusted > 30000


def test_category_rule_no_category():
    rule = CategoryPricingRule()
    adjusted, note = rule.apply(30000, None)
    assert adjusted == 30000
    assert note == ""


def test_pricing_decision_create():
    decision = PricingDecision.create(
        book_reference="REF-001",
        suggested_price=30000,
        explanation="Test explanation",
        condition_factor=0.7,
        reference_count=0,
    )
    assert decision.book_reference == "REF-001"
    assert decision.suggested_price == 30000
    assert decision.id is not None


def test_price_reference_create():
    ref = PriceReference.create(
        source="ebay",
        external_price=25000,
        book_reference="REF-001",
    )
    assert ref.source == "ebay"
    assert ref.external_price == 25000
    assert ref.currency == "COP"
"""

test_router = """import pytest
from app.routers.pricing_router import router


def test_router_has_calculate_route():
    routes = [r.path for r in router.routes]
    assert "/pricing/calculate" in routes


def test_router_has_decisions_route():
    routes = [r.path for r in router.routes]
    assert "/pricing/decisions/{book_reference}" in routes


def test_router_has_all_decisions_route():
    routes = [r.path for r in router.routes]
    assert "/pricing/decisions" in routes


def test_router_has_health_route():
    routes = [r.path for r in router.routes]
    assert "/pricing/health" in routes
"""

migration = """from alembic import op
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
"""

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
        prefix="sqlalchemy.", poolclass=pool.NullPool,
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

alembic_ini = """[alembic]
script_location = alembic
prepend_sys_path = .
sqlalchemy.url = postgresql://bookflow:bookflow123@postgres:5432/pricing_db

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
    'app/domain/rules.py': rules,
    'app/domain/repositories.py': repositories,
    'app/domain/schemas.py': schemas,
    'app/infrastructure/models.py': models,
    'app/infrastructure/database.py': database,
    'app/infrastructure/repositories.py': infra_repo,
    'app/infrastructure/ebay_client.py': ebay_client,
    'app/application/use_cases.py': use_cases,
    'app/routers/pricing_router.py': router,
    'main.py': main,
    'Dockerfile': dockerfile,
    'alembic.ini': alembic_ini,
    'alembic/__init__.py': '',
    'alembic/env.py': alembic_env,
    'alembic/versions/__init__.py': '',
    'alembic/versions/pri001_create_pricing_tables.py': migration,
    'tests/test_pricing_rules.py': test_pricing,
    'tests/test_pricing_router.py': test_router,
}

for path, content in files.items():
    full = os.path.join(os.getcwd(), path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Created: {path}')

print('Pricing service done!')
