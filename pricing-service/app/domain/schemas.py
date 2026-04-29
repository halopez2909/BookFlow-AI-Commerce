from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PricingRequest(BaseModel):
    book_reference: str
    isbn: Optional[str] = None
    condition: str = "good"
    category: Optional[str] = None
    title: Optional[str] = None


class PricingDecisionResponse(BaseModel):
    id: str
    book_reference: str
    suggested_price: float
    explanation: str
    condition_factor: float
    reference_count: int
    created_at: datetime

    class Config:
        from_attributes = True


class PriceReferenceResponse(BaseModel):
    id: str
    source: str
    external_price: float
    currency: str
    observed_at: datetime
    book_reference: str

    class Config:
        from_attributes = True
