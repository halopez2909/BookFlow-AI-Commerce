from app.domain.repository_interface import RecommendationRepositoryInterface
from app.domain.catalog_interface import CatalogServiceInterface
from app.domain.recommendation import Recommendation
from typing import List, Dict, Any

class GetRecommendationsUseCase:
    def __init__(self, repository: RecommendationRepositoryInterface, catalog_service: CatalogServiceInterface):
        self.repository = repository
        self.catalog_service = catalog_service

    async def execute(self, user_id: str) -> Dict[str, Any]:
        # 1. Obtener o generar IDs de recomendaciones desde persistencia
        recommendations = await self.repository.get_by_user_id(user_id)
        
        if not recommendations:
            default_rec = Recommendation(
                id=1,
                user_id=user_id,
                recommended_books=[101, 102, 103],
                reason="Basado en tus preferencias de lectura de Systems Engineering"
            )
            await self.repository.save(default_rec)
            active_recommendation = default_rec
        else:
            active_recommendation = recommendations[0]

        # 2. Ir al puerto de catálogo a buscar la información real de esos IDs de libros
        books_details = await self.catalog_service.get_books_by_ids(active_recommendation.recommended_books)

        # 3. Retornar la respuesta integrada lista para el frontend
        return {
            "user_id": active_recommendation.user_id,
            "reason": active_recommendation.reason,
            "generated_at": active_recommendation.created_at.isoformat(),
            "books": books_details
        }