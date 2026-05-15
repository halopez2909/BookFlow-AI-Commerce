"""
Tests del AIClassifier (estrategia OpenAI). Mockeamos la API de OpenAI
con pytest-mock para no depender de la red ni de la API key.
"""
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.domain.intents import IntentType
from app.infrastructure.providers.intent_classifier import AIClassifier


def _build_completion(label: str) -> MagicMock:
    """Arma una respuesta simulada de OpenAI con el label como contenido."""
    completion = MagicMock()
    completion.choices = [MagicMock()]
    completion.choices[0].message.content = label
    return completion


@pytest.fixture
def ai_classifier(mocker) -> AIClassifier:
    classifier = AIClassifier(api_key="test-key", model="gpt-4o-mini", timeout=1.0)
    # Forzamos el client interno con un mock
    fake_client = MagicMock()
    fake_client.chat.completions.create = AsyncMock()
    classifier._client = fake_client
    return classifier


class TestAIClassifierHappyPath:
    async def test_recognizes_availability(self, ai_classifier):
        ai_classifier._client.chat.completions.create.return_value = _build_completion(
            "AVAILABILITY_CHECK"
        )
        intent = await ai_classifier.classify("¿tienen el libro X?")
        assert intent == IntentType.AVAILABILITY_CHECK

    async def test_recognizes_price(self, ai_classifier):
        ai_classifier._client.chat.completions.create.return_value = _build_completion(
            "PRICE_QUERY"
        )
        intent = await ai_classifier.classify("cuánto cuesta")
        assert intent == IntentType.PRICE_QUERY

    async def test_trims_extra_whitespace_and_punctuation(self, ai_classifier):
        ai_classifier._client.chat.completions.create.return_value = _build_completion(
            "  book_search\n"
        )
        intent = await ai_classifier.classify("libros de X")
        assert intent == IntentType.BOOK_SEARCH


class TestAIClassifierFallback:
    async def test_returns_unknown_when_label_is_garbage(self, ai_classifier):
        ai_classifier._client.chat.completions.create.return_value = _build_completion(
            "I don't know"
        )
        intent = await ai_classifier.classify("hola")
        assert intent == IntentType.UNKNOWN

    async def test_returns_unknown_when_api_raises(self, ai_classifier):
        from openai import OpenAIError
        ai_classifier._client.chat.completions.create.side_effect = OpenAIError(
            "timeout"
        )
        intent = await ai_classifier.classify("cualquier cosa")
        assert intent == IntentType.UNKNOWN

    async def test_returns_unknown_when_api_key_missing(self):
        classifier = AIClassifier(api_key="", model="gpt-4o-mini", timeout=1.0)
        intent = await classifier.classify("cualquier cosa")
        assert intent == IntentType.UNKNOWN