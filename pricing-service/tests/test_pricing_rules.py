import pytest
from app.domain.rules import ConditionPricingRule, CategoryPricingRule
from app.domain.entities import PricingDecision, PriceReference


def test_condition_rule_new():
    rule = ConditionPricingRule()
    price, factor, explanation = rule.apply("new")
    assert factor == 1.0
    assert price > 0
    assert "nuevo" in explanation.lower() or "new" in explanation.lower()


def test_condition_rule_good():
    rule = ConditionPricingRule()
    price, factor, explanation = rule.apply("good")
    assert factor == 0.70
    assert price > 0


def test_condition_rule_worn():
    rule = ConditionPricingRule()
    price, factor, explanation = rule.apply("worn")
    assert factor == 0.40


def test_condition_rule_damaged():
    rule = ConditionPricingRule()
    price, factor, explanation = rule.apply("damaged")
    assert factor == 0.20


def test_condition_rule_unknown_defaults_good():
    rule = ConditionPricingRule()
    price, factor, explanation = rule.apply("unknown_condition")
    assert factor == 0.70


def test_category_rule_textbook():
    rule = CategoryPricingRule()
    adjusted, note = rule.apply(30000, "textbook")
    assert adjusted > 30000


def test_category_rule_no_category():
    rule = CategoryPricingRule()
    adjusted, note = rule.apply(30000, None)
    assert adjusted == 30000
    assert note == ""


def test_pricing_decision_create():
    decision = PricingDecision.create(
        book_reference="REF-001",
        suggested_price=30000,
        explanation="Test explanation",
        condition_factor=0.7,
        reference_count=0,
    )
    assert decision.book_reference == "REF-001"
    assert decision.suggested_price == 30000
    assert decision.id is not None


def test_price_reference_create():
    ref = PriceReference.create(
        source="ebay",
        external_price=25000,
        book_reference="REF-001",
    )
    assert ref.source == "ebay"
    assert ref.external_price == 25000
    assert ref.currency == "COP"
