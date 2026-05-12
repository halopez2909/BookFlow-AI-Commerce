from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities import PricingDecision, PriceReference


class PricingDecisionRepository(ABC):
    @abstractmethod
    def save(self, decision: PricingDecision) -> PricingDecision:
        pass

    @abstractmethod
    def find_by_book_reference(self, book_reference: str) -> Optional[PricingDecision]:
        pass

    @abstractmethod
    def find_all(self) -> List[PricingDecision]:
        pass


class PriceReferenceRepository(ABC):
    @abstractmethod
    def save(self, reference: PriceReference) -> PriceReference:
        pass

    @abstractmethod
    def find_by_book_reference(self, book_reference: str) -> List[PriceReference]:
        pass
