import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class CategoryModel(Base):
    __tablename__ = "categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)
    books = relationship("BookModel", back_populates="category")


class BookModel(Base):
    __tablename__ = "books"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False, index=True)
    author = Column(String, nullable=False, index=True)
    publisher = Column(String, nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"), nullable=False)
    isbn = Column(String, nullable=True, unique=True)
    issn = Column(String, nullable=True)
    description = Column(String, nullable=True)
    cover_url = Column(String, nullable=True)
    publication_year = Column(Integer, nullable=True)
    volume = Column(String, nullable=True)
    enriched_flag = Column(Boolean, default=False)
    published_flag = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    category = relationship("CategoryModel", back_populates="books")
