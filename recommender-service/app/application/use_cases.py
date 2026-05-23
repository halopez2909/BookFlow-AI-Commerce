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
        target_book = await self.catalog_client.get_book(book_id)
        all_books = await self.catalog_client.get_catalog()

        book_ids = [b.id for b in all_books]
        inventory_stock = await self.inventory_client.check_availability(book_ids)

        for b in all_books:
            b.quantity_available = inventory_stock.get(b.id, 10)
        if target_book:
            target_book.quantity_available = inventory_stock.get(target_book.id, 10)

        eligible_catalog = [b for b in all_books if self.spec.is_satisfied_by(b)]

        if not target_book:
            return eligible_catalog[:limit]

        if strategy_name == "category":
            strategy = CategoryStrategy(self.catalog_client)
        elif strategy_name == "author":
            strategy = AuthorStrategy(self.catalog_client)
        elif strategy_name == "price":
            strategy = PriceRangeStrategy(self.catalog_client)
        else:
            strategy = CompositeStrategy([
                CategoryStrategy(self.catalog_client),
                AuthorStrategy(self.catalog_client),
                PriceRangeStrategy(self.catalog_client)
            ])

        # Filter eligible excluding target
        candidates = [b for b in eligible_catalog if b.id != target_book.id]

        # Use strategy on candidates directly
        if strategy_name in ["category", "author", "price"]:
            recommendations = strategy.recommend(target_book, limit)
        else:
            recommendations = []
            seen_ids = set()
            for b in candidates:
                if len(recommendations) >= limit:
                    break
                if b.id not in seen_ids:
                    seen_ids.add(b.id)
                    recommendations.append(b)

        return recommendations[:limit]


class GetPopularBooksUseCase:
    def __init__(self, catalog_client: CatalogClient):
        self.catalog_client = catalog_client

    async def execute(self, limit: int = 10) -> List[Book]:
        all_books = await self.catalog_client.get_catalog()
        return all_books[:limit]
