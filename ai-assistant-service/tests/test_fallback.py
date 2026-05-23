"""
Tests del FallbackClassifier: clasificación por keywords sin red.
Cubre los 4 intents + UNKNOWN.
"""
import pytest

from app.domain.intents import IntentType
from app.infrastructure.providers.fallback_classifier import FallbackClassifier


@pytest.fixture
def classifier() -> FallbackClassifier:
    return FallbackClassifier()


class TestFallbackClassifier:
    async def test_availability_intent(self, classifier):
        intent = await classifier.classify("¿tienen El principito disponible?")
        assert intent == IntentType.AVAILABILITY_CHECK

    async def test_price_intent(self, classifier):
        intent = await classifier.classify("cuánto cuesta Cien años de soledad")
        assert intent == IntentType.PRICE_QUERY

    async def test_book_info_intent(self, classifier):
        intent = await classifier.classify("cuéntame sobre Don Quijote")
        assert intent == IntentType.BOOK_INFO

    async def test_book_search_intent(self, classifier):
        intent = await classifier.classify("libros de García Márquez")
        assert intent == IntentType.BOOK_SEARCH

    async def test_unknown_for_irrelevant_input(self, classifier):
        intent = await classifier.classify("hola, ¿cómo estás?")
        assert intent == IntentType.UNKNOWN

    async def test_unknown_for_empty(self, classifier):
        intent = await classifier.classify("   ")
        assert intent == IntentType.UNKNOWN

    async def test_accents_are_normalized(self, classifier):
        # "Disponibilidad" con tilde debe seguir matcheando AVAILABILITY
        intent = await classifier.classify("hay disponibilidad de Rayuela")
        assert intent == IntentType.AVAILABILITY_CHECK