import uuid
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
        created_at: Optional[datetime] = None,
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
        self.created_at = created_at or datetime.utcnow()
