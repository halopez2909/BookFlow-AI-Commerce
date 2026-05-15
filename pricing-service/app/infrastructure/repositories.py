from typing import List, Optional
from sqlalchemy.orm import Session
from app.domain.entities import PricingDecision, PriceReference
from app.domain.repositories import PricingDecisionRepository, PriceReferenceRepository
from app.infrastructure.models import PricingDecisionModel, PriceReferenceModel
from datetime import datetime


class PricingDecisionRepositoryPostgres(PricingDecisionRepository):
    def __init__(self, db: Session):
        self.db = db

    def save(self, decision: PricingDecision) -> PricingDecision:
        existing = self.db.query(PricingDecisionModel).filter(
            PricingDecisionModel.book_reference == decision.book_reference
        ).first()
        if existing:
            existing.suggested_price = decision.suggested_price
            existing.explanation = decision.explanation
            existing.condition_factor = decision.condition_factor
            existing.reference_count = decision.reference_count
            existing.created_at = decision.created_at
            self.db.commit()
        else:
            model = PricingDecisionModel(
                id=decision.id,
                book_reference=decision.book_reference,
                suggested_price=decision.suggested_price,
                explanation=decision.explanation,
                condition_factor=decision.condition_factor,
                reference_count=decision.reference_count,
                created_at=decision.created_at,
            )
            self.db.add(model)
            self.db.commit()
        return decision

    def find_by_book_reference(self, book_reference: str) -> Optional[PricingDecision]:
        model = self.db.query(PricingDecisionModel).filter(
            PricingDecisionModel.book_reference == book_reference
        ).order_by(PricingDecisionModel.created_at.desc()).first()
        if not model:
            return None
        return PricingDecision(
            id=model.id, book_reference=model.book_reference,
            suggested_price=model.suggested_price, explanation=model.explanation,
            condition_factor=model.condition_factor, reference_count=model.reference_count,
            created_at=model.created_at,
        )

    def find_all(self) -> List[PricingDecision]:
        models = self.db.query(PricingDecisionModel).order_by(
            PricingDecisionModel.created_at.desc()
        ).all()
        return [PricingDecision(
            id=m.id, book_reference=m.book_reference,
            suggested_price=m.suggested_price, explanation=m.explanation,
            condition_factor=m.condition_factor, reference_count=m.reference_count,
            created_at=m.created_at,
        ) for m in models]


class PriceReferenceRepositoryPostgres(PriceReferenceRepository):
    def __init__(self, db: Session):
        self.db = db

    def save(self, reference: PriceReference) -> PriceReference:
        model = PriceReferenceModel(
            id=reference.id, source=reference.source,
            external_price=reference.external_price, currency=reference.currency,
            observed_at=reference.observed_at, book_reference=reference.book_reference,
        )
        self.db.add(model)
        self.db.commit()
        return reference

    def find_by_book_reference(self, book_reference: str) -> List[PriceReference]:
        models = self.db.query(PriceReferenceModel).filter(
            PriceReferenceModel.book_reference == book_reference
        ).all()
        return [PriceReference(
            id=m.id, source=m.source, external_price=m.external_price,
            currency=m.currency, observed_at=m.observed_at, book_reference=m.book_reference,
        ) for m in models]
