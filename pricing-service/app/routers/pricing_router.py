from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.domain.schemas import PricingRequest, PricingDecisionResponse
from app.infrastructure.repositories import PricingDecisionRepositoryPostgres, PriceReferenceRepositoryPostgres
from app.infrastructure.database import get_db
from app.application.use_cases import CalculatePrice, GetPricingDecision, GetAllDecisions
from typing import List

router = APIRouter(prefix="/pricing", tags=["pricing"])


@router.post("/calculate", response_model=PricingDecisionResponse, status_code=201)
async def calculate_price(request: PricingRequest, db: Session = Depends(get_db)):
    try:
        decision_repo = PricingDecisionRepositoryPostgres(db)
        reference_repo = PriceReferenceRepositoryPostgres(db)
        use_case = CalculatePrice(decision_repo, reference_repo)
        decision = await use_case.execute(
            book_reference=request.book_reference,
            isbn=request.isbn,
            condition=request.condition,
            category=request.category,
            title=request.title,
        )
        return PricingDecisionResponse(
            id=decision.id, book_reference=decision.book_reference,
            suggested_price=decision.suggested_price, explanation=decision.explanation,
            condition_factor=decision.condition_factor, reference_count=decision.reference_count,
            created_at=decision.created_at,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/decisions/{book_reference}", response_model=PricingDecisionResponse)
def get_decision(book_reference: str, db: Session = Depends(get_db)):
    try:
        repo = PricingDecisionRepositoryPostgres(db)
        use_case = GetPricingDecision(repo)
        decision = use_case.execute(book_reference)
        if not decision:
            raise HTTPException(status_code=404, detail="No pricing decision found")
        return PricingDecisionResponse(
            id=decision.id, book_reference=decision.book_reference,
            suggested_price=decision.suggested_price, explanation=decision.explanation,
            condition_factor=decision.condition_factor, reference_count=decision.reference_count,
            created_at=decision.created_at,
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/decisions", response_model=List[PricingDecisionResponse])
def get_all_decisions(db: Session = Depends(get_db)):
    try:
        repo = PricingDecisionRepositoryPostgres(db)
        use_case = GetAllDecisions(repo)
        decisions = use_case.execute()
        return [PricingDecisionResponse(
            id=d.id, book_reference=d.book_reference,
            suggested_price=d.suggested_price, explanation=d.explanation,
            condition_factor=d.condition_factor, reference_count=d.reference_count,
            created_at=d.created_at,
        ) for d in decisions]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
def health():
    return {"status": "ok", "service": "pricing-service"}
