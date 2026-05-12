import uuid
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

    def find_all(self, title, author, category_id, page, page_size, min_price=None, max_price=None, available=None):
        query = self.db.query(BookModel)
        if title:
            query = query.filter(BookModel.title.ilike(f"%{title}%"))
        if author:
            query = query.filter(BookModel.author.ilike(f"%{author}%"))
        if category_id:
            query = query.filter(BookModel.category_id == category_id)
        if min_price is not None:
            query = query.filter(BookModel.suggested_price >= min_price)
        if max_price is not None:
            query = query.filter(BookModel.suggested_price <= max_price)
        if available is not None:
            query = query.filter(BookModel.published_flag == available)
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
