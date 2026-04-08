from pydantic import BaseModel, field_validator
from typing import Optional, List
import uuid


class BookCreateRequest(BaseModel):
    title: str
    author: str
    publisher: str
    category_id: uuid.UUID
    isbn: Optional[str] = None
    issn: Optional[str] = None
    description: Optional[str] = None
    cover_url: Optional[str] = None
    publication_year: Optional[int] = None
    volume: Optional[str] = None

    @field_validator("isbn")
    @classmethod
    def validate_isbn(cls, v):
        if v is None:
            return v
        clean = v.replace("-", "").replace(" ", "")
        if len(clean) not in (10, 13) or not clean.isdigit():
            raise ValueError("ISBN must be 10 or 13 digits")
        return clean

    @field_validator("issn")
    @classmethod
    def validate_issn(cls, v):
        if v is None:
            return v
        if len(v) != 9 or v[4] != "-":
            raise ValueError("ISSN must have format XXXX-XXXX")
        return v


class BookResponse(BaseModel):
    id: uuid.UUID
    title: str
    author: str
    publisher: str
    category_id: uuid.UUID
    isbn: Optional[str] = None
    issn: Optional[str] = None
    description: Optional[str] = None
    cover_url: Optional[str] = None
    publication_year: Optional[int] = None
    volume: Optional[str] = None
    enriched_flag: bool
    published_flag: bool

    model_config = {"from_attributes": True}


class BookListResponse(BaseModel):
    items: List[BookResponse]
    total: int
    page: int
    page_size: int


class CategoryCreateRequest(BaseModel):
    name: str
    description: Optional[str] = None


class CategoryResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: Optional[str] = None

    model_config = {"from_attributes": True}
