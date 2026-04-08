from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.domain.schemas import CategoryCreateRequest, CategoryResponse
from app.application.use_cases import RegisterCategory, ListCategories
from app.infrastructure.repositories import CategoryRepositoryPostgres
from app.infrastructure.database import get_db

router = APIRouter(prefix="/catalog/categories", tags=["categories"])


def get_register_category(db: Session = Depends(get_db)) -> RegisterCategory:
    return RegisterCategory(CategoryRepositoryPostgres(db))


def get_list_categories(db: Session = Depends(get_db)) -> ListCategories:
    return ListCategories(CategoryRepositoryPostgres(db))


@router.post("", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def register_category(
    request: CategoryCreateRequest,
    use_case: RegisterCategory = Depends(get_register_category),
):
    return use_case.execute(request)


@router.get("", response_model=List[CategoryResponse])
def list_categories(
    use_case: ListCategories = Depends(get_list_categories),
):
    return use_case.execute()
