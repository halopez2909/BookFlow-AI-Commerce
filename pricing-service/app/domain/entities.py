from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import uuid


@dataclass(frozen=True)
class PriceReference:
    id: str
    source: str
    external_price: float
    currency: str
    observed_at: datetime
    book_reference: str

    @staticmethod
    def create(source: str, external_price: float, book_reference: str, currency: str = "COP") -> "PriceReference":
        return PriceReference(
            id=str(uuid.uuid4()),
            source=source,
            external_price=external_price,
            currency=currency,
            observed_at=datetime.utcnow(),
            book_reference=book_reference,
        )


@dataclass(frozen=True)
class PricingDecision:
    id: str
    book_reference: str
    suggested_price: float
    explanation: str
    condition_factor: float
    reference_count: int
    created_at: datetime

    @staticmethod
    def create(
        book_reference: str,
        suggested_price: float,
        explanation: str,
        condition_factor: float,
        reference_count: int,
    ) -> "PricingDecision":
        return PricingDecision(
            id=str(uuid.uuid4()),
            book_reference=book_reference,
            suggested_price=suggested_price,
            explanation=explanation,
            condition_factor=condition_factor,
            reference_count=reference_count,
            created_at=datetime.utcnow(),
        )
