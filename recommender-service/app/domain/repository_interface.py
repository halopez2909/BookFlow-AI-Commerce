from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.recommendation import Recommendation

class RecommendationRepositoryInterface(ABC):
    
    @abstractmethod
    async def save(self, recommendation: Recommendation) -> Recommendation:
        """Guarda una nueva recomendación en el sistema de persistencia."""
        pass

    @abstractmethod
    async def get_by_user_id(self, user_id: str) -> List[Recommendation]:
        """Recupera el historial de recomendaciones otorgadas a un usuario."""
        pass

    @abstractmethod
    async def get_by_id(self, recommendation_id: int) -> Optional[Recommendation]:
        """Busca una recomendación específica por su ID único."""
        pass