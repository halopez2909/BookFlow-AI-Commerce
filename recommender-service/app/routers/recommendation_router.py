from fastapi import APIRouter, HTTPException
from app.application.get_recommendations import GetRecommendationsUseCase
from app.infrastructure.memory_repository import InMemoryRecommendationRepository
from app.infrastructure.http_catalog_client import HttpCatalogClient

router = APIRouter(prefix="/api/recommendations", tags=["Recommendations"])

# Instanciamos los adaptadores de infraestructura
repository = InMemoryRecommendationRepository()
catalog_client = HttpCatalogClient()

@router.get("/{user_id}")
async def get_user_recommendations(user_id: str):
    try:
        # Inyectamos ambos adaptadores en el caso de uso
        use_case = GetRecommendationsUseCase(repository, catalog_client)
        result = await use_case.execute(user_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))