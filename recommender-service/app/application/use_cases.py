from typing import List, Optional
from app.domain.models import Book
from app.domain.specifications import EligibilitySpecification
from app.domain.strategies import (
    CategoryStrategy, 
    AuthorStrategy, 
    PriceRangeStrategy, 
    CompositeStrategy
)
from app.infrastructure.clients.catalog_client import CatalogClient
from app.infrastructure.clients.inventory_client import InventoryClient

class GetRecommendationsUseCase:
    def __init__(self, catalog_client: CatalogClient, inventory_client: InventoryClient):
        self.catalog_client = catalog_client
        self.inventory_client = inventory_client
        self.spec = EligibilitySpecification()

    async def execute(self, book_id: str, strategy_name: Optional[str] = None, limit: int = 6) -> List[Book]:
        # 1. Obtener el libro objetivo y el catálogo completo externo
        target_book = await self.catalog_client.get_book(book_id)
        all_books = await self.catalog_client.get_catalog()

        # 2. Validar stock en tiempo real con el inventario
        book_ids = [b.id for b in all_books]
        inventory_stock = await self.inventory_client.check_availability(book_ids)
        
        # Sincronizar el stock en nuestros objetos de dominio
        for b in all_books:
            b.quantity_available = inventory_stock.get(b.id, 0)
        if target_book:
            target_book.quantity_available = inventory_stock.get(target_book.id, 0)

        # 3. Filtrar candidatos elegibles del catálogo usando Specification Pattern (Stock > 0 y Publicado)
        eligible_catalog = [b for b in all_books if self.spec.is_satisfied_by(b)]

        if not target_book:
            return eligible_catalog[:limit]

        # 4. Seleccionar la estrategia solicitada (Strategy & Composite Pattern)
        if strategy_name == "category":
            strategy = CategoryStrategy()
        elif strategy_name == "author":
            strategy = AuthorStrategy()
        elif strategy_name == "price":
            strategy = PriceRangeStrategy()
        else:
            # Estrategia por defecto: Combina todas las anteriores (Composite)
            strategy = CompositeStrategy([
                CategoryStrategy(),
                AuthorStrategy(),
                PriceRangeStrategy()
            ])

        # 5. Obtener recomendaciones iniciales
        recommendations = strategy.recommend(target_book, eligible_catalog, limit)

        # 6. Mecanismo de Relleno (Criterio 7): Si faltan libros, rellenar con la misma categoría ordenados por precio
        if len(recommendations) < limit:
            category_fallback = [
                b for b in eligible_catalog 
                if b.category == target_book.category 
                and b.id != target_book.id 
                and b not in recommendations
            ]
            # Ordenar por precio de menor a mayor
            category_fallback.sort(key=lambda x: x.price)
            
            for fallback_book in category_fallback:
                recommendations.append(fallback_book)
                if len(recommendations) >= limit:
                    break

        return recommendations[:limit]


class GetPopularBooksUseCase:
    def __init__(self, catalog_client: CatalogClient):
        self.catalog_client = catalog_client

    async def execute(self, limit: int = 10) -> List[Book]:
        # Simula la lectura de logs de assistant_db retornando el top 10 del catálogo
        all_books = await self.catalog_client.get_catalog()
        return all_books[:limit]