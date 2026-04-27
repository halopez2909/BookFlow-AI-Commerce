from sqlalchemy import Column, String, Boolean, DateTime
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
