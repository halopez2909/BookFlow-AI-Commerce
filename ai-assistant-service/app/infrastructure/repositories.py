"""
Implementación SQLAlchemy del AssistantInteractionRepository.
Mapea ORM <-> entidad de dominio.
"""
from typing import List

from sqlalchemy.orm import Session

from app.domain.entities import AssistantInteraction
from app.domain.intents import IntentType
from app.domain.repositories import AssistantInteractionRepository
from app.infrastructure.models import AssistantInteractionORM


class AssistantInteractionRepositoryPostgres(AssistantInteractionRepository):
    def __init__(self, db: Session) -> None:
        self.db = db

    # ---------- mappers ----------
    @staticmethod
    def _to_entity(orm: AssistantInteractionORM) -> AssistantInteraction:
        return AssistantInteraction(
            id=orm.id,
            session_id=orm.session_id,
            user_question=orm.user_question,
            interpreted_intent=IntentType(orm.interpreted_intent),
            answer_text=orm.answer_text,
            created_at=orm.created_at,
        )

    @staticmethod
    def _to_orm(entity: AssistantInteraction) -> AssistantInteractionORM:
        return AssistantInteractionORM(
            id=entity.id,
            session_id=entity.session_id,
            user_question=entity.user_question,
            interpreted_intent=entity.interpreted_intent.value,
            answer_text=entity.answer_text,
            created_at=entity.created_at,
        )

    # ---------- API pública ----------
    def save(self, interaction: AssistantInteraction) -> AssistantInteraction:
        orm = self._to_orm(interaction)
        self.db.add(orm)
        self.db.commit()
        self.db.refresh(orm)
        return self._to_entity(orm)

    def list_by_session(self, session_id: str) -> List[AssistantInteraction]:
        rows = (
            self.db.query(AssistantInteractionORM)
            .filter(AssistantInteractionORM.session_id == session_id)
            .order_by(AssistantInteractionORM.created_at.asc())
            .all()
        )
        return [self._to_entity(r) for r in rows]