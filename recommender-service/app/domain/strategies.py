# app/domain/strategies.py
from typing import Protocol, List
from app.domain.models import Book

class RecommendationStrategy(Protocol):
    def recommend(self, book: Book, limit: int) -> List[Book]:
        ...

class CategoryStrategy:
    def __init__(self, catalog_client):
        self.catalog_client = catalog_client

    def recommend(self, book: Book, limit: int) -> List[Book]:
        # Busca libros de la misma categoría, excluyendo el libro actual
        books = self.catalog_client.get_by_category(book.category)
        return [b for b in books if b.id != book.id][:limit]

class AuthorStrategy:
    def __init__(self, catalog_client):
        self.catalog_client = catalog_client

    def recommend(self, book: Book, limit: int) -> List[Book]:
        books = self.catalog_client.get_by_author(book.author)
        return [b for b in books if b.id != book.id][:limit]

class PriceRangeStrategy:
    def __init__(self, catalog_client):
        self.catalog_client = catalog_client

    def recommend(self, book: Book, limit: int) -> List[Book]:
        min_price = book.price * 0.70
        max_price = book.price * 1.30
        books = self.catalog_client.get_by_price_range(min_price, max_price)
        return [b for b in books if b.id != book.id][:limit]

class CompositeStrategy:
    def __init__(self, strategies: List[RecommendationStrategy]):
        self.strategies = strategies

    def recommend(self, book: Book, limit: int) -> List[Book]:
        results = []
        seen_ids = set()
        
        for strategy in self.strategies:
            if len(results) >= limit:
                break
            
            candidates = strategy.recommend(book, limit)
            for candidate in candidates:
                if candidate.id not in seen_ids and len(results) < limit:
                    seen_ids.add(candidate.id)
                    results.append(candidate)
                    
        return results