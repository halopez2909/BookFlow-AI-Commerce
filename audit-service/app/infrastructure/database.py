import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from app.infrastructure.models import Base

load_dotenv()

# ── Base de datos propia ──
AUDIT_DATABASE_URL = os.getenv("AUDIT_DATABASE_URL")

# ── Sprint 2 — solo lectura ──
PRICING_DATABASE_URL = os.getenv("PRICING_DATABASE_URL")
ENRICHMENT_DATABASE_URL = os.getenv("ENRICHMENT_DATABASE_URL")

# ── Sprint 3 — solo lectura ──
ORDER_DATABASE_URL = os.getenv("ORDER_DATABASE_URL")
ASSISTANT_DATABASE_URL = os.getenv("ASSISTANT_DATABASE_URL")

# Engines
audit_engine = create_engine(AUDIT_DATABASE_URL)
pricing_engine = create_engine(PRICING_DATABASE_URL)
enrichment_engine = create_engine(ENRICHMENT_DATABASE_URL)
order_engine = create_engine(ORDER_DATABASE_URL)
assistant_engine = create_engine(ASSISTANT_DATABASE_URL)

# Sessions
AuditSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=audit_engine)
PricingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=pricing_engine)
EnrichmentSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=enrichment_engine)
OrderSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=order_engine)
AssistantSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=assistant_engine)


def create_tables():
    """Solo crea las tablas propias del audit-service en audit_db."""
    Base.metadata.create_all(bind=audit_engine)


# ── Dependency injectors para FastAPI ──

def get_audit_db():
    db = AuditSessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_pricing_db():
    db = PricingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_enrichment_db():
    db = EnrichmentSessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_order_db():
    db = OrderSessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_assistant_db():
    db = AssistantSessionLocal()
    try:
        yield db
    finally:
        db.close()
