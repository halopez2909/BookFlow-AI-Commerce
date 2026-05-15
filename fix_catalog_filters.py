# Fix repositories.py - add price and available filters
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
"""

# Fix use_cases.py - add price and available filters
use_cases = """import uuid
from datetime import datetime
from typing import Optional, List
from app.domain.entities import Book, Category
from app.domain.repositories import BookRepository, CategoryRepository
from app.domain.schemas import BookCreateRequest, BookResponse, BookListResponse, CategoryCreateRequest, CategoryResponse


class RegisterBook:
    def __init__(self, repository: BookRepository):
        self.repository = repository

    def execute(self, request: BookCreateRequest) -> BookResponse:
        book = Book(
            id=uuid.uuid4(), title=request.title, author=request.author,
            publisher=request.publisher, category_id=request.category_id,
            isbn=request.isbn, issn=request.issn, description=request.description,
            cover_url=request.cover_url, publication_year=request.publication_year,
            volume=request.volume, created_at=datetime.utcnow(),
        )
        saved = self.repository.save(book)
        return self._to_response(saved)

    def _to_response(self, book: Book) -> BookResponse:
        return BookResponse(
            id=book.id, title=book.title, author=book.author,
            publisher=book.publisher, category_id=book.category_id,
            isbn=book.isbn, issn=book.issn, description=book.description,
            cover_url=book.cover_url, publication_year=book.publication_year,
            volume=book.volume, enriched_flag=book.enriched_flag,
            published_flag=book.published_flag, suggested_price=book.suggested_price,
        )


class GetBookById:
    def __init__(self, repository: BookRepository):
        self.repository = repository

    def execute(self, book_id: uuid.UUID) -> BookResponse:
        book = self.repository.get_by_id(book_id)
        if not book:
            raise ValueError("BOOK_NOT_FOUND")
        return BookResponse(
            id=book.id, title=book.title, author=book.author,
            publisher=book.publisher, category_id=book.category_id,
            isbn=book.isbn, issn=book.issn, description=book.description,
            cover_url=book.cover_url, publication_year=book.publication_year,
            volume=book.volume, enriched_flag=book.enriched_flag,
            published_flag=book.published_flag, suggested_price=book.suggested_price,
        )


class ListBooks:
    def __init__(self, repository: BookRepository):
        self.repository = repository

    def execute(self, title, author, category_id, page, page_size, min_price=None, max_price=None, available=None) -> BookListResponse:
        books, total = self.repository.find_all(title, author, category_id, page, page_size, min_price, max_price, available)
        items = [
            BookResponse(
                id=b.id, title=b.title, author=b.author,
                publisher=b.publisher, category_id=b.category_id,
                isbn=b.isbn, issn=b.issn, description=b.description,
                cover_url=b.cover_url, publication_year=b.publication_year,
                volume=b.volume, enriched_flag=b.enriched_flag,
                published_flag=b.published_flag, suggested_price=b.suggested_price,
            )
            for b in books
        ]
        return BookListResponse(items=items, total=total, page=page, page_size=page_size)


class PublishBook:
    def __init__(self, repository: BookRepository):
        self.repository = repository

    def execute(self, book_id: uuid.UUID) -> BookResponse:
        book = self.repository.get_by_id(book_id)
        if not book:
            raise ValueError("BOOK_NOT_FOUND")
        missing = []
        if not book.title: missing.append("title")
        if not book.author: missing.append("author")
        if not book.category_id: missing.append("category_id")
        if missing:
            raise ValueError(f"MISSING_FIELDS:{','.join(missing)}")
        published = self.repository.publish(book_id)
        return BookResponse(
            id=published.id, title=published.title, author=published.author,
            publisher=published.publisher, category_id=published.category_id,
            isbn=published.isbn, issn=published.issn, description=published.description,
            cover_url=published.cover_url, publication_year=published.publication_year,
            volume=published.volume, enriched_flag=published.enriched_flag,
            published_flag=published.published_flag, suggested_price=published.suggested_price,
        )


class RegisterCategory:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def execute(self, request: CategoryCreateRequest) -> CategoryResponse:
        category = Category(id=uuid.uuid4(), name=request.name, description=request.description)
        saved = self.repository.save(category)
        return CategoryResponse(id=saved.id, name=saved.name, description=saved.description)


class ListCategories:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def execute(self) -> List[CategoryResponse]:
        categories = self.repository.get_all()
        return [CategoryResponse(id=c.id, name=c.name, description=c.description) for c in categories]
"""

# Fix routers
routers = """from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from app.infrastructure.repositories import BookRepositoryPostgres, CategoryRepositoryPostgres
from app.application.use_cases import RegisterBook, GetBookById, ListBooks, PublishBook, RegisterCategory, ListCategories
from app.domain.schemas import BookCreateRequest, CategoryCreateRequest
from app.infrastructure.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/catalog/books")
def list_books(
    title: Optional[str] = None,
    author: Optional[str] = None,
    category_id: Optional[str] = None,
    page: int = 1,
    page_size: int = 20,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    available: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    repo = BookRepositoryPostgres(db)
    use_case = ListBooks(repo)
    import uuid
    cat_id = uuid.UUID(category_id) if category_id else None
    return use_case.execute(title, author, cat_id, page, page_size, min_price, max_price, available)

@router.get("/catalog/books/{book_id}")
def get_book(book_id: str, db: Session = Depends(get_db)):
    import uuid
    repo = BookRepositoryPostgres(db)
    use_case = GetBookById(repo)
    try:
        return use_case.execute(uuid.UUID(book_id))
    except ValueError:
        raise HTTPException(status_code=404, detail="Book not found")

@router.post("/catalog/books", status_code=201)
def create_book(book_data: BookCreateRequest, db: Session = Depends(get_db)):
    repo = BookRepositoryPostgres(db)
    use_case = RegisterBook(repo)
    return use_case.execute(book_data)

@router.post("/catalog/books/{book_id}/publish")
def publish_book(book_id: str, db: Session = Depends(get_db)):
    import uuid
    repo = BookRepositoryPostgres(db)
    use_case = PublishBook(repo)
    try:
        return use_case.execute(uuid.UUID(book_id))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/catalog/categories")
def list_categories(db: Session = Depends(get_db)):
    repo = CategoryRepositoryPostgres(db)
    use_case = ListCategories(repo)
    return use_case.execute()

@router.post("/catalog/categories", status_code=201)
def create_category(category_data: CategoryCreateRequest, db: Session = Depends(get_db)):
    repo = CategoryRepositoryPostgres(db)
    use_case = RegisterCategory(repo)
    return use_case.execute(category_data)
"""

with open("catalog-service/app/infrastructure/repositories.py", "w", encoding="utf-8") as f:
    f.write(repositories)
print("repositories.py updated")

with open("catalog-service/app/application/use_cases.py", "w", encoding="utf-8") as f:
    f.write(use_cases)
print("use_cases.py updated")

# Check if routers file exists
import os
router_files = []
for root, dirs, files in os.walk("catalog-service/app"):
    for f in files:
        if "router" in f.lower() or "route" in f.lower():
            router_files.append(os.path.join(root, f))
print("Router files found:", router_files)
