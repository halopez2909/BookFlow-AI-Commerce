import uuid
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
            id=uuid.uuid4(),
            title=request.title,
            author=request.author,
            publisher=request.publisher,
            category_id=request.category_id,
            isbn=request.isbn,
            issn=request.issn,
            description=request.description,
            cover_url=request.cover_url,
            publication_year=request.publication_year,
            volume=request.volume,
            created_at=datetime.utcnow(),
        )
        saved = self.repository.save(book)
        return self._to_response(saved)

    def _to_response(self, book: Book) -> BookResponse:
        return BookResponse(
            id=book.id,
            title=book.title,
            author=book.author,
            publisher=book.publisher,
            category_id=book.category_id,
            isbn=book.isbn,
            issn=book.issn,
            description=book.description,
            cover_url=book.cover_url,
            publication_year=book.publication_year,
            volume=book.volume,
            enriched_flag=book.enriched_flag,
            published_flag=book.published_flag,
        )


class GetBookById:

    def __init__(self, repository: BookRepository):
        self.repository = repository

    def execute(self, book_id: uuid.UUID) -> BookResponse:
        book = self.repository.get_by_id(book_id)
        if not book:
            raise ValueError("BOOK_NOT_FOUND")
        return BookResponse(
            id=book.id,
            title=book.title,
            author=book.author,
            publisher=book.publisher,
            category_id=book.category_id,
            isbn=book.isbn,
            issn=book.issn,
            description=book.description,
            cover_url=book.cover_url,
            publication_year=book.publication_year,
            volume=book.volume,
            enriched_flag=book.enriched_flag,
            published_flag=book.published_flag,
        )


class ListBooks:

    def __init__(self, repository: BookRepository):
        self.repository = repository

    def execute(self, title: Optional[str], author: Optional[str], category_id: Optional[uuid.UUID], page: int, page_size: int) -> BookListResponse:
        books, total = self.repository.find_all(title, author, category_id, page, page_size)
        items = [
            BookResponse(
                id=b.id,
                title=b.title,
                author=b.author,
                publisher=b.publisher,
                category_id=b.category_id,
                isbn=b.isbn,
                issn=b.issn,
                description=b.description,
                cover_url=b.cover_url,
                publication_year=b.publication_year,
                volume=b.volume,
                enriched_flag=b.enriched_flag,
                published_flag=b.published_flag,
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
        if not book.title:
            missing.append("title")
        if not book.author:
            missing.append("author")
        if not book.category_id:
            missing.append("category_id")
        if missing:
            raise ValueError(f"MISSING_FIELDS:{','.join(missing)}")
        published = self.repository.publish(book_id)
        return BookResponse(
            id=published.id,
            title=published.title,
            author=published.author,
            publisher=published.publisher,
            category_id=published.category_id,
            isbn=published.isbn,
            issn=published.issn,
            description=published.description,
            cover_url=published.cover_url,
            publication_year=published.publication_year,
            volume=published.volume,
            enriched_flag=published.enriched_flag,
            published_flag=published.published_flag,
        )


class RegisterCategory:

    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def execute(self, request: CategoryCreateRequest) -> CategoryResponse:
        category = Category(
            id=uuid.uuid4(),
            name=request.name,
            description=request.description,
        )
        saved = self.repository.save(category)
        return CategoryResponse(id=saved.id, name=saved.name, description=saved.description)


class ListCategories:

    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def execute(self) -> List[CategoryResponse]:
        categories = self.repository.get_all()
        return [CategoryResponse(id=c.id, name=c.name, description=c.description) for c in categories]
