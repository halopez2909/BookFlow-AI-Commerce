"""
ResponseBuilder: arma el texto natural de respuesta a partir de
los datos reales consultados. No conoce HTTP ni base de datos.
Reglas:
  - Si no hay datos del libro → mensaje 'no encontrado' (no inventa).
  - Si falta un dato puntual → lo dice ('no se pudo confirmar').
  - Pluraliza listas de búsqueda.
"""
from typing import List, Optional

from app.domain.entities import BookSnapshot
from app.domain.intents import IntentType


class ResponseBuilder:
    # ---------- availability ----------
    def build_availability(
        self,
        query: str,
        book: Optional[BookSnapshot],
        stock: Optional[dict],
    ) -> str:
        if book is None:
            return (
                f'No encontré "{query}" en el catálogo. '
                "Es posible que no lo manejemos. ¿Quieres que busque algo similar?"
            )
        title = book.title or query
        if stock is None:
            return (
                f'Encontré "{title}" en el catálogo, pero no pude confirmar el '
                "stock con el servicio de inventario en este momento."
            )
        if stock.get("available"):
            qty = stock.get("quantity", 0)
            return f'Sí, "{title}" está disponible. Tenemos {qty} unidades en stock.'
        return f'Lo siento, "{title}" no está disponible en este momento.'

    # ---------- price ----------
    def build_price(
        self,
        query: str,
        book: Optional[BookSnapshot],
        pricing: Optional[dict],
    ) -> str:
        if book is None:
            return f'No encontré "{query}" en el catálogo, así que no puedo darte un precio.'
        title = book.title or query
        # 1° intentamos pricing service, 2° caemos al suggested_price del catálogo
        price = (pricing or {}).get("price") if pricing else None
        currency = (pricing or {}).get("currency", "COP")
        if price is None:
            price = book.price
        if price is None:
            return f'Encontré "{title}", pero aún no tiene un precio publicado.'
        return f'El precio de "{title}" es {price:,.0f} {currency}.'

    # ---------- book info ----------
    def build_book_info(self, query: str, book: Optional[BookSnapshot]) -> str:
        if book is None:
            return f'No encontré información sobre "{query}" en el catálogo.'
        parts: List[str] = []
        if book.title:
            parts.append(f'"{book.title}"')
        if book.author:
            parts.append(f"de {book.author}")
        header = " ".join(parts) if parts else query
        if book.description:
            return f"{header}: {book.description}"
        return f"Encontré {header}, pero todavía no tenemos descripción registrada."

    # ---------- search ----------
    def build_search(self, query: str, results: List[BookSnapshot]) -> str:
        if not results:
            return f'No encontré libros que coincidan con "{query}".'
        lines = [f"Encontré {len(results)} libro(s) relacionados con \"{query}\":"]
        for b in results[:5]:
            title = b.title or "(sin título)"
            author = f" — {b.author}" if b.author else ""
            lines.append(f"• {title}{author}")
        return "\n".join(lines)

    # ---------- fallback ----------
    def build_unknown(self, query: str) -> str:
        return (
            "No estoy seguro de qué me preguntas. Puedo ayudarte con "
            "disponibilidad, precio, descripción de un libro o búsqueda "
            "por autor. ¿Puedes reformular la pregunta?"
        )

    # ---------- dispatcher (opcional, útil para tests) ----------
    def build(
        self,
        intent: IntentType,
        query: str,
        book: Optional[BookSnapshot] = None,
        stock: Optional[dict] = None,
        pricing: Optional[dict] = None,
        results: Optional[List[BookSnapshot]] = None,
    ) -> str:
        if intent == IntentType.AVAILABILITY_CHECK:
            return self.build_availability(query, book, stock)
        if intent == IntentType.PRICE_QUERY:
            return self.build_price(query, book, pricing)
        if intent == IntentType.BOOK_INFO:
            return self.build_book_info(query, book)
        if intent == IntentType.BOOK_SEARCH:
            return self.build_search(query, results or [])
        return self.build_unknown(query)