from abc import ABC, abstractmethod
from typing import Optional, List
import uuid
from app.domain.entities import Book, Category


class BookRepository(ABC):

    @abstractmethod
    def save(self, book: Book) -> Book:
        pass

    @abstractmethod
    def get_by_id(self, book_id: uuid.UUID) -> Optional[Book]:
        pass

    @abstractmethod
    def find_all(self, title: Optional[str], author: Optional[str], category_id: Optional[uuid.UUID], page: int, page_size: int) -> tuple[List[Book], int]:
        pass

    @abstractmethod
    def publish(self, book_id: uuid.UUID) -> Book:
        pass

    @abstractmethod
    def update(self, book: Book) -> Book:
        pass


class CategoryRepository(ABC):

    @abstractmethod
    def save(self, category: Category) -> Category:
        pass

    @abstractmethod
    def get_all(self) -> List[Category]:
        pass

    @abstractmethod
    def get_by_id(self, category_id: uuid.UUID) -> Optional[Category]:
        pass
