"""
Casos de uso de la capa application. ProcessQuery es la cadena
principal (Chain of Responsibility):
  1) clasificar intención (AIClassifier; si UNKNOWN, FallbackClassifier).
  2) extraer la entidad (título/autor) de la pregunta.
  3) consultar los servicios necesarios según la intención.
  4) construir la respuesta con ResponseBuilder.
  5) persistir la interacción.
  6) devolver answer, intent y sources.
"""
import asyncio
import re
import unicodedata
from typing import List

from app.domain.entities import AssistantInteraction, BookSnapshot
from app.domain.intent_classifier import IntentClassifier
from app.domain.intents import IntentType
from app.domain.repositories import AssistantInteractionRepository
from app.domain.response_builder import ResponseBuilder
from app.infrastructure.clients.catalog_client import CatalogClient
from app.infrastructure.clients.inventory_client import InventoryClient
from app.infrastructure.clients.pricing_client import PricingClient


# ---------- helper: extraer entidad de la pregunta ----------

_STOPWORDS_PREFIX = [
    "tienen", "tienes", "hay", "cuanto cuesta", "cuánto cuesta",
    "cuanto vale", "cuánto vale", "precio de", "cuentame sobre",
    "cuéntame sobre", "hablame de", "háblame de", "informacion sobre",
    "información sobre", "sobre", "libros de", "obras de", "novelas de",
    "buscar", "muéstrame", "muestrame", "el libro", "el", "la", "los",
    "las", "un", "una",
]

# Palabras finales irrelevantes (las quitamos al final de la pregunta)
_STOPWORDS_SUFFIX = [
    "disponible", "disponibles", "disponibilidad",
    "en stock", "stock", "ahora", "hoy",
]


def _strip_accents(text: str) -> str:
    text = unicodedata.normalize("NFD", text)
    return "".join(ch for ch in text if unicodedata.category(ch) != "Mn")


def extract_entity(question: str) -> str:
    """
    Heurística simple para sacar el nombre del libro/autor de la
    pregunta. Quita signos, baja a minúsculas, recorta prefijos
    típicos. No es perfecto, pero alcanza para llamar al catalog.
    """
    q = question.strip().lstrip("¿¡!?").rstrip("?!.,").strip()
    q_low = _strip_accents(q.lower())
    for sw in sorted(_STOPWORDS_PREFIX, key=len, reverse=True):
        sw_norm = _strip_accents(sw)
        # Quita el prefijo si la pregunta empieza con él
        pattern = rf"^{re.escape(sw_norm)}\b\s*"
        q_low = re.sub(pattern, "", q_low, count=1)
    # Quita sufijos irrelevantes ("disponible", "en stock", etc.)
    for sw in sorted(_STOPWORDS_SUFFIX, key=len, reverse=True):
        sw_norm = _strip_accents(sw)
        pattern = rf"\s*\b{re.escape(sw_norm)}\b\s*$"
        q_low = re.sub(pattern, "", q_low, count=1)
    original_words = q.split()
    cleaned_words = q_low.split()
    if not cleaned_words:
        return q
    # Buscar la posición de la primera palabra limpia dentro de las
    # originales (case-insensitive y accent-insensitive) y tomar N
    # palabras consecutivas desde ahí.
    n = len(cleaned_words)
    first_clean = cleaned_words[0]
    for i, w in enumerate(original_words):
        if _strip_accents(w.lower()) == first_clean:
            return " ".join(original_words[i:i + n]).strip()
    # Fallback: si no encontramos un match, devolvemos las últimas N palabras
    return " ".join(original_words[-n:]).strip()


# ---------- Use Case principal ----------

class ProcessQuery:
    def __init__(
        self,
        ai_classifier: IntentClassifier,
        fallback_classifier: IntentClassifier,
        catalog_client: CatalogClient,
        inventory_client: InventoryClient,
        pricing_client: PricingClient,
        response_builder: ResponseBuilder,
        repository: AssistantInteractionRepository,
    ) -> None:
        self.ai = ai_classifier
        self.fallback = fallback_classifier
        self.catalog = catalog_client
        self.inventory = inventory_client
        self.pricing = pricing_client
        self.builder = response_builder
        self.repo = repository

    async def _classify(self, question: str) -> IntentType:
        intent = await self.ai.classify(question)
        if intent == IntentType.UNKNOWN:
            return await self.fallback.classify(question)
        return intent

    async def _resolve_book(self, entity: str) -> BookSnapshot | None:
        results = await self.catalog.search_by_title(entity, limit=1)
        return results[0] if results else None

    async def execute(self, session_id: str, question: str) -> dict:
        intent = await self._classify(question)
        entity = extract_entity(question)
        sources: List[str] = []
        answer: str

        if intent == IntentType.AVAILABILITY_CHECK:
            book = await self._resolve_book(entity)
            sources.append("catalog")
            stock = None
            if book is not None:
                stock = await self.inventory.get_stock(book.book_id)
                sources.append("inventory")
            answer = self.builder.build_availability(entity, book, stock)

        elif intent == IntentType.PRICE_QUERY:
            book = await self._resolve_book(entity)
            sources.append("catalog")
            pricing = None
            if book is not None:
                pricing = await self.pricing.get_price(book.book_id)
                sources.append("pricing")
            answer = self.builder.build_price(entity, book, pricing)

        elif intent == IntentType.BOOK_INFO:
            book = await self._resolve_book(entity)
            sources.append("catalog")
            answer = self.builder.build_book_info(entity, book)

        elif intent == IntentType.BOOK_SEARCH:
            # Buscamos por autor primero; si vacío, intentamos por título
            results = await self.catalog.search_by_author(entity, limit=10)
            if not results:
                results = await self.catalog.search_by_title(entity, limit=10)
            sources.append("catalog")
            answer = self.builder.build_search(entity, results)

        else:
            answer = self.builder.build_unknown(question)

        # Persistir la interacción
        interaction = AssistantInteraction(
            session_id=session_id,
            user_question=question,
            interpreted_intent=intent,
            answer_text=answer,
        )
        self.repo.save(interaction)

        return {"answer": answer, "intent": intent, "sources": sources}


# ---------- Use Case: historial por sesión ----------

class GetSessionHistory:
    def __init__(self, repository: AssistantInteractionRepository) -> None:
        self.repo = repository

    def execute(self, session_id: str) -> List[AssistantInteraction]:
        return self.repo.list_by_session(session_id)