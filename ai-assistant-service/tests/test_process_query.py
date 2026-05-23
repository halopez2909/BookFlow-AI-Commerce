"""
Tests del ProcessQuery (orquestador). Cubre los 4 escenarios
obligatorios del documento de Sprint 3:
  - consulta de disponibilidad
  - consulta de precio
  - libro no encontrado en el catálogo
  - fallback cuando la API de IA falla
"""
from typing import List
from unittest.mock import AsyncMock

import pytest

from app.application.use_cases import ProcessQuery
from app.domain.entities import BookSnapshot
from app.domain.intent_classifier import IntentClassifier
from app.domain.intents import IntentType


# ---------- Stubs de clasificadores ----------

class StubClassifier(IntentClassifier):
    """Retorna siempre el intent que se le pase en construcción."""

    def __init__(self, intent: IntentType) -> None:
        self.intent = intent

    async def classify(self, question: str) -> IntentType:
        return self.intent


# ---------- Helpers ----------

def _build_clients(
    book: BookSnapshot | None = None,
    stock: dict | None = None,
    pricing: dict | None = None,
    search_results: List[BookSnapshot] | None = None,
):
    catalog = AsyncMock()
    catalog.search_by_title = AsyncMock(return_value=[book] if book else [])
    catalog.search_by_author = AsyncMock(return_value=search_results or [])
    catalog.get_by_id = AsyncMock(return_value=book)

    inventory = AsyncMock()
    inventory.get_stock = AsyncMock(return_value=stock)

    pricing_client = AsyncMock()
    pricing_client.get_price = AsyncMock(return_value=pricing)

    return catalog, inventory, pricing_client


# ---------- Tests ----------

class TestProcessQueryAvailability:
    async def test_book_in_stock(self, repo, builder):
        book = BookSnapshot(book_id="b1", title="El principito", author="Saint-Exupéry")
        catalog, inventory, pricing = _build_clients(
            book=book, stock={"available": True, "quantity": 5}
        )
        use_case = ProcessQuery(
            ai_classifier=StubClassifier(IntentType.AVAILABILITY_CHECK),
            fallback_classifier=StubClassifier(IntentType.UNKNOWN),
            catalog_client=catalog,
            inventory_client=inventory,
            pricing_client=pricing,
            response_builder=builder,
            repository=repo,
        )
        result = await use_case.execute("s1", "¿tienen El principito?")

        assert result["intent"] == IntentType.AVAILABILITY_CHECK
        assert "disponible" in result["answer"].lower()
        assert "5 unidades" in result["answer"]
        assert "catalog" in result["sources"]
        assert "inventory" in result["sources"]
        # Se persistió en el repo
        assert len(repo.items) == 1
        assert repo.items[0].interpreted_intent == IntentType.AVAILABILITY_CHECK


class TestProcessQueryPrice:
    async def test_returns_price_from_pricing_service(self, repo, builder):
        book = BookSnapshot(book_id="b2", title="Cien años de soledad", price=None)
        catalog, inventory, pricing = _build_clients(
            book=book, pricing={"price": 45000.0, "currency": "COP", "explanation": ""}
        )
        use_case = ProcessQuery(
            ai_classifier=StubClassifier(IntentType.PRICE_QUERY),
            fallback_classifier=StubClassifier(IntentType.UNKNOWN),
            catalog_client=catalog,
            inventory_client=inventory,
            pricing_client=pricing,
            response_builder=builder,
            repository=repo,
        )
        result = await use_case.execute("s1", "cuánto cuesta Cien años de soledad")

        assert result["intent"] == IntentType.PRICE_QUERY
        assert "45,000" in result["answer"] or "45000" in result["answer"]
        assert "COP" in result["answer"]
        assert "pricing" in result["sources"]


class TestProcessQueryNotFound:
    async def test_book_not_found_does_not_invent(self, repo, builder):
        catalog, inventory, pricing = _build_clients(book=None)
        use_case = ProcessQuery(
            ai_classifier=StubClassifier(IntentType.AVAILABILITY_CHECK),
            fallback_classifier=StubClassifier(IntentType.UNKNOWN),
            catalog_client=catalog,
            inventory_client=inventory,
            pricing_client=pricing,
            response_builder=builder,
            repository=repo,
        )
        result = await use_case.execute("s1", "¿tienen libro_inexistente?")

        # No debe inventar disponibilidad ni stock
        assert "no encontré" in result["answer"].lower()
        # Y no debe haber llamado a inventory porque no había book
        inventory.get_stock.assert_not_called()


class TestProcessQueryFallbackOnAIFailure:
    async def test_falls_back_to_keyword_classifier_when_ai_returns_unknown(
        self, repo, builder
    ):
        book = BookSnapshot(book_id="b3", title="Rayuela")
        catalog, inventory, pricing = _build_clients(
            book=book, stock={"available": True, "quantity": 3}
        )
        # AI simula caída → devuelve UNKNOWN. Fallback debe activarse.
        use_case = ProcessQuery(
            ai_classifier=StubClassifier(IntentType.UNKNOWN),
            fallback_classifier=StubClassifier(IntentType.AVAILABILITY_CHECK),
            catalog_client=catalog,
            inventory_client=inventory,
            pricing_client=pricing,
            response_builder=builder,
            repository=repo,
        )
        result = await use_case.execute("s1", "¿tienen Rayuela?")

        # El intent final viene del fallback, no del AI
        assert result["intent"] == IntentType.AVAILABILITY_CHECK
        assert "disponible" in result["answer"].lower()