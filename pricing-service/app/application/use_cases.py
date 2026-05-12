from typing import Optional
from app.domain.entities import PricingDecision, PriceReference
from app.domain.repositories import PricingDecisionRepository, PriceReferenceRepository
from app.domain.rules import ConditionPricingRule, CategoryPricingRule
from app.infrastructure.ebay_client import EbayPriceClient


class CalculatePrice:
    def __init__(
        self,
        decision_repo: PricingDecisionRepository,
        reference_repo: PriceReferenceRepository,
    ):
        self.decision_repo = decision_repo
        self.reference_repo = reference_repo
        self.condition_rule = ConditionPricingRule()
        self.category_rule = CategoryPricingRule()
        self.ebay_client = EbayPriceClient()

    async def execute(
        self,
        book_reference: str,
        isbn: Optional[str] = None,
        condition: str = "good",
        category: Optional[str] = None,
        title: Optional[str] = None,
    ) -> PricingDecision:
        ebay_price = await self.ebay_client.get_reference_price(isbn, title)

        ref_count = 0
        if ebay_price:
            ref = PriceReference.create(
                source="ebay", external_price=ebay_price, book_reference=book_reference
            )
            self.reference_repo.save(ref)
            ref_count = 1

        suggested, factor, explanation = self.condition_rule.apply(condition, ebay_price)
        cat_adjusted, cat_note = self.category_rule.apply(suggested, category)
        final_price = cat_adjusted
        full_explanation = explanation + cat_note

        if ebay_price:
            full_explanation += f" Referencia eBay:  COP."
        else:
            full_explanation += " Sin referencia externa disponible. Precio basado en reglas internas."

        decision = PricingDecision.create(
            book_reference=book_reference,
            suggested_price=final_price,
            explanation=full_explanation,
            condition_factor=factor,
            reference_count=ref_count,
        )
        return self.decision_repo.save(decision)


class GetPricingDecision:
    def __init__(self, repo: PricingDecisionRepository):
        self.repo = repo

    def execute(self, book_reference: str) -> Optional[PricingDecision]:
        return self.repo.find_by_book_reference(book_reference)


class GetAllDecisions:
    def __init__(self, repo: PricingDecisionRepository):
        self.repo = repo

    def execute(self):
        return self.repo.find_all()
