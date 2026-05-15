"""
Enum de intenciones que el asistente puede reconocer.

Sigue el contrato de Sprint 3: cada pregunta del usuario se clasifica
en exactamente uno de estos tipos. UNKNOWN es el Null Object: cuando
no se puede clasificar con confianza, se retorna este valor en lugar
de lanzar una excepción.
"""
from enum import Enum


class IntentType(str, Enum):
    AVAILABILITY_CHECK = "AVAILABILITY_CHECK"   # "¿tienen El principito?"
    PRICE_QUERY = "PRICE_QUERY"                 # "¿cuánto cuesta X?"
    BOOK_INFO = "BOOK_INFO"                     # "cuéntame sobre X"
    BOOK_SEARCH = "BOOK_SEARCH"                 # "libros de García Márquez"
    UNKNOWN = "UNKNOWN"                         # fallback Null Object


# Mapeo de palabras clave por intención. Lo usa el FallbackClassifier
# cuando la API de IA no está disponible.
INTENT_KEYWORDS: dict[IntentType, list[str]] = {
    IntentType.AVAILABILITY_CHECK: [
        "tienen", "tienes", "hay", "disponible", "disponibilidad",
        "stock", "queda", "quedan", "existencia",
    ],
    IntentType.PRICE_QUERY: [
        "cuánto cuesta", "cuanto cuesta", "precio", "vale", "cuesta",
        "valor", "cuánto vale", "cuanto vale",
    ],
    IntentType.BOOK_INFO: [
        "cuéntame", "cuentame", "háblame", "hablame", "información",
        "informacion", "sobre", "de qué trata", "de que trata",
        "sinopsis", "resumen", "describe",
    ],
    IntentType.BOOK_SEARCH: [
        "libros de", "obras de", "novelas de", "buscar", "muéstrame",
        "muestrame", "qué libros", "que libros",
    ],
}