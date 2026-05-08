# Fix entities.py
entities = """import uuid
from datetime import datetime
from typing import Optional

class ISBN:
    def __init__(self, value: str):
        clean = value.replace("-", "").replace(" ", "")
        if len(clean) not in (10, 13) or not clean.isdigit():
            raise ValueError(f"Invalid ISBN: {value}")
        self.value = clean
    def __str__(self):
        return self.value

class ISSN:
    def __init__(self, value: str):
        if not value or len(value) != 9 or value[4] != "-":
            raise ValueError(f"Invalid ISSN format: {value}")
        self.value = value
    def __str__(self):
        return self.value

class Category:
    def __init__(self, id: uuid.UUID, name: str, description: Optional[str] = None):
        self.id = id
        self.name = name
        self.description = description

class Book:
    def __init__(
        self,
        id: uuid.UUID,
        title: str,
        author: str,
        publisher: str,
        category_id: uuid.UUID,
        isbn: Optional[str] = None,
        issn: Optional[str] = None,
        description: Optional[str] = None,
        cover_url: Optional[str] = None,
        publication_year: Optional[int] = None,
        volume: Optional[str] = None,
        enriched_flag: bool = False,
        published_flag: bool = False,
        suggested_price: Optional[float] = None,
        created_at=None,
    ):
        self.id = id
        self.title = title
        self.author = author
        self.publisher = publisher
        self.category_id = category_id
        self.isbn = isbn
        self.issn = issn
        self.description = description
        self.cover_url = cover_url
        self.publication_year = publication_year
        self.volume = volume
        self.enriched_flag = enriched_flag
        self.published_flag = published_flag
        self.suggested_price = suggested_price
        self.created_at = created_at or datetime.utcnow()
"""

# Fix repositories.py
repositories = """import uuid
from typing import Optional, List
from sqlalchemy.orm import Session
from app.domain.entities import Book, Category
from app.domain.repositories import BookRepository, CategoryRepository
from app.infrastructure.models import BookModel, CategoryModel


class BookRepositoryPostgres(BookRepository):

    def __init__(self, db: Session):
        self.db = db

    def save(self, book: Book) -> Book:
        model = BookModel(
            id=book.id, title=book.title, author=book.author,
            publisher=book.publisher, category_id=book.category_id,
            isbn=book.isbn, issn=book.issn, description=book.description,
            cover_url=book.cover_url, publication_year=book.publication_year,
            volume=book.volume, enriched_flag=book.enriched_flag,
            published_flag=book.published_flag, created_at=book.created_at,
            suggested_price=book.suggested_price,
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return self._to_entity(model)

    def get_by_id(self, book_id: uuid.UUID) -> Optional[Book]:
        model = self.db.query(BookModel).filter(BookModel.id == book_id).first()
        return self._to_entity(model) if model else None

    def find_all(self, title, author, category_id, page, page_size):
        query = self.db.query(BookModel)
        if title:
            query = query.filter(BookModel.title.ilike(f"%{title}%"))
        if author:
            query = query.filter(BookModel.author.ilike(f"%{author}%"))
        if category_id:
            query = query.filter(BookModel.category_id == category_id)
        total = query.count()
        models = query.offset((page - 1) * page_size).limit(page_size).all()
        return [self._to_entity(m) for m in models], total

    def publish(self, book_id: uuid.UUID) -> Book:
        model = self.db.query(BookModel).filter(BookModel.id == book_id).first()
        model.published_flag = True
        self.db.commit()
        self.db.refresh(model)
        return self._to_entity(model)

    def update(self, book: Book) -> Book:
        model = self.db.query(BookModel).filter(BookModel.id == book.id).first()
        model.title = book.title
        model.author = book.author
        model.publisher = book.publisher
        model.description = book.description
        model.cover_url = book.cover_url
        model.publication_year = book.publication_year
        model.volume = book.volume
        model.enriched_flag = book.enriched_flag
        model.suggested_price = book.suggested_price
        self.db.commit()
        self.db.refresh(model)
        return self._to_entity(model)

    def _to_entity(self, model: BookModel) -> Book:
        return Book(
            id=model.id, title=model.title, author=model.author,
            publisher=model.publisher, category_id=model.category_id,
            isbn=model.isbn, issn=model.issn, description=model.description,
            cover_url=model.cover_url, publication_year=model.publication_year,
            volume=model.volume, enriched_flag=model.enriched_flag,
            published_flag=model.published_flag, created_at=model.created_at,
            suggested_price=float(model.suggested_price) if model.suggested_price else None,
        )


class CategoryRepositoryPostgres(CategoryRepository):

    def __init__(self, db: Session):
        self.db = db

    def save(self, category: Category) -> Category:
        model = CategoryModel(id=category.id, name=category.name, description=category.description)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return self._to_entity(model)

    def get_all(self) -> List[Category]:
        return [self._to_entity(m) for m in self.db.query(CategoryModel).all()]

    def get_by_id(self, category_id: uuid.UUID) -> Optional[Category]:
        model = self.db.query(CategoryModel).filter(CategoryModel.id == category_id).first()
        return self._to_entity(model) if model else None

    def _to_entity(self, model: CategoryModel) -> Category:
        return Category(id=model.id, name=model.name, description=model.description)
"""

with open("catalog-service/app/domain/entities.py", "w", encoding="utf-8") as f:
    f.write(entities)
print("entities.py updated")

with open("catalog-service/app/infrastructure/repositories.py", "w", encoding="utf-8") as f:
    f.write(repositories)
print("repositories.py updated")
