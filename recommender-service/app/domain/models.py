# app/domain/models.py
from pydantic import BaseModel
from typing import Optional

class Book(BaseModel):
    id: str
    title: str
    author: str
    category: str
    price: float
    published_flag: bool
    quantity_available: int