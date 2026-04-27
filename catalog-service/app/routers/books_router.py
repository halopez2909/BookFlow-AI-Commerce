import uuid
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.domain.schemas import BookCreateRequest, BookResponse, BookListResponse
from app.application.use_cases import RegisterBook, GetBookById, ListBooks, PublishBook
from app.infrastructure.repositories import BookRepositoryPostgres
from app.infrastructure.database import get_db

router = APIRouter(prefix="/catalog/books", tags=["books"])


def get_register_book(db: Session = Depends(get_db)) -> RegisterBook:
    return RegisterBook(BookRepositoryPostgres(db))


def get_book_by_id(db: Session = Depends(get_db)) -> GetBookById:
    return GetBookById(BookRepositoryPostgres(db))


def get_list_books(db: Session = Depends(get_db)) -> ListBooks:
    return ListBooks(BookRepositoryPostgres(db))


def get_publish_book(db: Session = Depends(get_db)) -> PublishBook:
    return PublishBook(BookRepositoryPostgres(db))


@router.post("", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def register_book(
    request: BookCreateRequest,
    use_case: RegisterBook = Depends(get_register_book),
):
    return use_case.execute(request)


@router.get("", response_model=BookListResponse)
def list_books(
    title: Optional[str] = None,
    author: Optional[str] = None,
    category_id: Optional[uuid.UUID] = None,
    page: int = 1,
    page_size: int = 20,
    use_case: ListBooks = Depends(get_list_books),
):
    return use_case.execute(title, author, category_id, page, page_size)


@router.get("/{book_id}", response_model=BookResponse)
def get_book(
    book_id: uuid.UUID,
    use_case: GetBookById = Depends(get_book_by_id),
):
    try:
        return use_case.execute(book_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@router.put("/{book_id}", response_model=BookResponse)
def update_book(
    book_id: uuid.UUID,
    request: BookCreateRequest,
    db: Session = Depends(get_db),
):
    repo = BookRepositoryPostgres(db)
    book = repo.get_by_id(book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    book.title = request.title
    book.author = request.author
    book.publisher = request.publisher
    book.description = request.description
    book.cover_url = request.cover_url
    book.publication_year = request.publication_year
    book.volume = request.volume
    updated = repo.update(book)
    return updated


@router.post("/{book_id}/publish", response_model=BookResponse)
def publish_book(
    book_id: uuid.UUID,
    use_case: PublishBook = Depends(get_publish_book),
):
    try:
        return use_case.execute(book_id)
    except ValueError as e:
        error = str(e)
        if error == "BOOK_NOT_FOUND":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
        if error.startswith("MISSING_FIELDS"):
            fields = error.split(":")[1]
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Missing required fields: {fields}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
