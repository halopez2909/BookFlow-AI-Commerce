# app/domain/specifications.py
from app.domain.models import Book

class EligibilitySpecification:
    def is_satisfied_by(self, book: Book) -> bool:
        return book.quantity_available > 0 and book.published_flag is True

    def filter(self, books: list[Book]) -> list[Book]:
        return [book for book in books if self.is_satisfied_by(book)]