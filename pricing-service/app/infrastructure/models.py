from sqlalchemy import Column, String, Float, Integer, DateTime
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
