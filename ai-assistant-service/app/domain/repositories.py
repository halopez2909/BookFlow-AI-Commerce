"""
Contratos (interfaces) de repositorios. El dominio NUNCA depende de
SQLAlchemy: depende de estas interfaces. Las implementaciones viven
en app/infrastructure/repositories.py.
"""
from abc import ABC, abstractmethod
from typing import List

from app.domain.entities import AssistantInteraction


class AssistantInteractionRepository(ABC):
    @abstractmethod
    def save(self, interaction: AssistantInteraction) -> AssistantInteraction:
        """Persiste una interacción y la devuelve (con id y created_at)."""
        raise NotImplementedError

    @abstractmethod
    def list_by_session(self, session_id: str) -> List[AssistantInteraction]:
        """Devuelve todas las interacciones de una sesión, ordenadas por created_at asc."""
        raise NotImplementedError