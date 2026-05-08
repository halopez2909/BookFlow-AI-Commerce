from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.infrastructure.database import get_db
from app.infrastructure.repositories import BookRepositoryPostgres
from app.application.use_cases import RegisterBook, GetBookById, ListBooks, PublishBook
from app.domain.schemas import BookCreateRequest
import uuid

router = APIRouter(prefix="/catalog/books", tags=["books"])

@router.get("")
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
    cat_id = uuid.UUID(category_id) if category_id else None
    return ListBooks(repo).execute(title, author, cat_id, page, page_size, min_price, max_price, available)

@router.get("/{book_id}")
def get_book(book_id: str, db: Session = Depends(get_db)):
    repo = BookRepositoryPostgres(db)
    try:
        return GetBookById(repo).execute(uuid.UUID(book_id))
    except ValueError:
        raise HTTPException(status_code=404, detail="Book not found")

@router.post("", status_code=201)
def create_book(book_data: BookCreateRequest, db: Session = Depends(get_db)):
    repo = BookRepositoryPostgres(db)
    return RegisterBook(repo).execute(book_data)

@router.post("/{book_id}/publish")
def publish_book(book_id: str, db: Session = Depends(get_db)):
    repo = BookRepositoryPostgres(db)
    try:
        return PublishBook(repo).execute(uuid.UUID(book_id))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
