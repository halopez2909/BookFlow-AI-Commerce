"""
Modelos ORM SQLAlchemy. Son la representación TÉCNICA de las
entidades del dominio. NUNCA se exponen fuera de infrastructure:
el repositorio los mapea hacia/desde las entidades del dominio.
"""
from datetime import datetime

from sqlalchemy import Column, DateTime, Index, String, Text

from app.infrastructure.database import Base


class AssistantInteractionORM(Base):
    __tablename__ = "assistant_interactions"

    id = Column(String(36), primary_key=True)
    session_id = Column(String(128), nullable=False, index=True)
    user_question = Column(Text, nullable=False)
    interpreted_intent = Column(String(32), nullable=False)
    answer_text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (
        Index("ix_assistant_interactions_session_created", "session_id", "created_at"),
    )