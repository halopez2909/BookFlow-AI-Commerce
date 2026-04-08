import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class ImportBatchModel(Base):
    __tablename__ = "import_batches"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    file_name = Column(String, nullable=False)
    upload_date = Column(DateTime, default=datetime.utcnow)
    total_rows = Column(Integer, default=0)
    valid_rows = Column(Integer, default=0)
    invalid_rows = Column(Integer, default=0)
    status = Column(String, nullable=False, default="processing")
    items = relationship("InventoryItemModel", back_populates="batch")
    errors = relationship("ImportErrorModel", back_populates="batch")


class InventoryItemModel(Base):
    __tablename__ = "inventory_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    external_code = Column(String, nullable=False)
    book_reference = Column(String, nullable=False, index=True)
    quantity_available = Column(Integer, default=0)
    quantity_reserved = Column(Integer, default=0)
    condition = Column(String, nullable=False)
    defects = Column(String, nullable=True)
    observations = Column(String, nullable=True)
    import_batch_id = Column(UUID(as_uuid=True), ForeignKey("import_batches.id"), nullable=False)
    batch = relationship("ImportBatchModel", back_populates="items")


class ImportErrorModel(Base):
    __tablename__ = "import_errors"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    batch_id = Column(UUID(as_uuid=True), ForeignKey("import_batches.id"), nullable=False)
    row_number = Column(Integer, nullable=False)
    error_type = Column(String, nullable=False)
    message = Column(String, nullable=False)
    batch = relationship("ImportBatchModel", back_populates="errors")
