"""
FallbackClassifier: estrategia que clasifica usando palabras clave
(regex/contains). No depende de red ni de API externas. Aplica el
Null Object Pattern: si no puede clasificar, retorna UNKNOWN en
lugar de lanzar excepción.
"""
import re
import unicodedata

from app.domain.intent_classifier import IntentClassifier
from app.domain.intents import INTENT_KEYWORDS, IntentType


def _normalize(text: str) -> str:
    """Pasa a minúsculas y quita tildes para hacer matching robusto."""
    text = text.lower().strip()
    text = unicodedata.normalize("NFD", text)
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    # Colapsa espacios múltiples
    text = re.sub(r"\s+", " ", text)
    return text


def _strip_accents_keyword(kw: str) -> str:
    kw = kw.lower()
    kw = unicodedata.normalize("NFD", kw)
    return "".join(ch for ch in kw if unicodedata.category(ch) != "Mn")


class FallbackClassifier(IntentClassifier):
    """
    Implementación de IntentClassifier basada en keywords. Cuenta cuántas
    palabras clave de cada intención aparecen en la pregunta normalizada
    y elige la intención con más matches.
    """

    async def classify(self, question: str) -> IntentType:
        if not question or not question.strip():
            return IntentType.UNKNOWN

        normalized = _normalize(question)

        scores: dict[IntentType, int] = {intent: 0 for intent in INTENT_KEYWORDS}
        for intent, keywords in INTENT_KEYWORDS.items():
            for kw in keywords:
                kw_norm = _strip_accents_keyword(kw)
                # Si la keyword tiene espacios, busca como frase
                if " " in kw_norm:
                    if kw_norm in normalized:
                        scores[intent] += 2  # frases pesan más
                else:
                    # Coincidencia de palabra completa
                    if re.search(rf"\b{re.escape(kw_norm)}\b", normalized):
                        scores[intent] += 1

        best_intent, best_score = max(scores.items(), key=lambda kv: kv[1])
        if best_score == 0:
            return IntentType.UNKNOWN
        return best_intent