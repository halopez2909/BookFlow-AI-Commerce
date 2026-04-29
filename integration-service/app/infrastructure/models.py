from sqlalchemy import Column, String, Integer, DateTime, JSON
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
