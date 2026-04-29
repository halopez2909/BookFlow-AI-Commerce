import os
from enum import Enum
from typing import Optional


class BookCondition(str, Enum):
    NEW = "new"
    GOOD = "good"
    WORN = "worn"
    DAMAGED = "damaged"


CONDITION_FACTORS = {
    BookCondition.NEW: 1.0,
    BookCondition.GOOD: 0.70,
    BookCondition.WORN: 0.40,
    BookCondition.DAMAGED: 0.20,
}

BASE_PRICES = {
    BookCondition.NEW: float(os.getenv("BASE_PRICE_NEW", "45000")),
    BookCondition.GOOD: float(os.getenv("BASE_PRICE_GOOD", "30000")),
    BookCondition.WORN: float(os.getenv("BASE_PRICE_WORN", "15000")),
    BookCondition.DAMAGED: float(os.getenv("BASE_PRICE_DAMAGED", "8000")),
}

CATEGORY_MULTIPLIERS = {
    "textbook": 1.3,
    "technical": 1.2,
    "fiction": 0.9,
    "children": 0.8,
    "default": 1.0,
}


class ConditionPricingRule:
    def apply(self, condition: str, base_price: Optional[float] = None) -> tuple[float, float, str]:
        try:
            cond = BookCondition(condition.lower())
        except ValueError:
            cond = BookCondition.GOOD

        factor = CONDITION_FACTORS[cond]
        price = base_price or BASE_PRICES[cond]
        final = round(price * factor, -2)

        explanations = {
            BookCondition.NEW: f"Libro nuevo. Factor: {factor}. Precio base:  COP.",
            BookCondition.GOOD: f"Buen estado. Factor de descuento: {factor} ({int((1-factor)*100)}% menos). Base:  COP.",
            BookCondition.WORN: f"Estado desgastado. Factor: {factor} ({int((1-factor)*100)}% descuento). Base:  COP.",
            BookCondition.DAMAGED: f"Libro daniado. Factor minimo: {factor} ({int((1-factor)*100)}% descuento). Base:  COP.",
        }

        return final, factor, explanations[cond]


class CategoryPricingRule:
    def apply(self, suggested_price: float, category: Optional[str]) -> tuple[float, str]:
        if not category:
            return suggested_price, ""
        mult = CATEGORY_MULTIPLIERS.get(category.lower(), CATEGORY_MULTIPLIERS["default"])
        if mult == 1.0:
            return suggested_price, ""
        adjusted = round(suggested_price * mult, -2)
        return adjusted, f" Ajuste por categoria '{category}': x{mult}."
