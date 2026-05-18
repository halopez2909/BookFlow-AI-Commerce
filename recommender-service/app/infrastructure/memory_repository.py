from app.domain.repository_interface import RecommendationRepositoryInterface
from app.domain.recommendation import Recommendation
from typing import List, Optional

class InMemoryRecommendationRepository(RecommendationRepositoryInterface):
    def __init__(self):
        self._storage = {}
        self._current_id = 1

    async def save(self, recommendation: Recommendation) -> Recommendation:
        if recommendation.id is None:
            recommendation.id = self._current_id
            self._current_id += 1
        self._storage[recommendation.id] = recommendation
        return recommendation

    async def get_by_user_id(self, user_id: str) -> List[Recommendation]:
        return [rec for rec in self._storage.values() if rec.user_id == user_id]

    async def get_by_id(self, recommendation_id: int) -> Optional[Recommendation]:
        return self._storage.get(recommendation_id)