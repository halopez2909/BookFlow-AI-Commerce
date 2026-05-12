import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from app.infrastructure.models import Base

load_dotenv()

# Base de datos propia del audit-service
AUDIT_DATABASE_URL = os.getenv("AUDIT_DATABASE_URL")

# Bases de datos externas (solo lectura)
PRICING_DATABASE_URL = os.getenv("PRICING_DATABASE_URL")
ENRICHMENT_DATABASE_URL = os.getenv("ENRICHMENT_DATABASE_URL")

audit_engine = create_engine(AUDIT_DATABASE_URL)
AuditSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=audit_engine)

pricing_engine = create_engine(PRICING_DATABASE_URL)
PricingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=pricing_engine)

enrichment_engine = create_engine(ENRICHMENT_DATABASE_URL)
EnrichmentSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=enrichment_engine)


def create_tables():
    Base.metadata.create_all(bind=audit_engine)


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
