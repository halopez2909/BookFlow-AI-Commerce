"""
Fixtures comunes para los tests. Implementaciones in-memory de los
repositorios para no necesitar Postgres en CI.
"""
from typing import List

import pytest

from app.domain.entities import AssistantInteraction
from app.domain.repositories import AssistantInteractionRepository
from app.domain.response_builder import ResponseBuilder


class InMemoryInteractionRepo(AssistantInteractionRepository):
    """Repositorio en memoria — para tests, sin Postgres."""

    def __init__(self) -> None:
        self.items: List[AssistantInteraction] = []

    def save(self, interaction: AssistantInteraction) -> AssistantInteraction:
        self.items.append(interaction)
        return interaction

    def list_by_session(self, session_id: str) -> List[AssistantInteraction]:
        return [i for i in self.items if i.session_id == session_id]


@pytest.fixture
def repo() -> InMemoryInteractionRepo:
    return InMemoryInteractionRepo()


@pytest.fixture
def builder() -> ResponseBuilder:
    return ResponseBuilder()