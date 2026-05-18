"""
AIClassifier: estrategia que usa la API de OpenAI para clasificar
la intención. Si la API falla (timeout, error, sin API key),
captura la excepción y retorna IntentType.UNKNOWN para que el caller
pueda decidir caer al FallbackClassifier.
"""
import logging
import os

from openai import AsyncOpenAI, OpenAIError

from app.domain.intent_classifier import IntentClassifier
from app.domain.intents import IntentType

logger = logging.getLogger(__name__)

_SYSTEM_PROMPT = (
    "Eres un clasificador de intenciones para un asistente de librería. "
    "Dada una pregunta del usuario, responde EXACTAMENTE con UNA de "
    "estas etiquetas (sin comillas, sin explicaciones, sin puntuación):\n"
    "AVAILABILITY_CHECK - el usuario pregunta si un libro está disponible o en stock.\n"
    "PRICE_QUERY - el usuario pregunta el precio o costo de un libro.\n"
    "BOOK_INFO - el usuario pide descripción, sinopsis o detalles de un libro.\n"
    "BOOK_SEARCH - el usuario busca libros por autor, categoría o tema.\n"
    "UNKNOWN - no encaja en ninguna de las anteriores."
)


class AIClassifier(IntentClassifier):
    """
    Implementación de IntentClassifier basada en OpenAI Chat Completions.
    """

    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None,
        timeout: float | None = None,
    ) -> None:
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "")
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.timeout = timeout or float(os.getenv("AI_TIMEOUT", "4"))
        self._client: AsyncOpenAI | None = None

    def _get_client(self) -> AsyncOpenAI:
        if not self.api_key:
            raise OpenAIError("OPENAI_API_KEY no está configurada")
        if self._client is None:
            self._client = AsyncOpenAI(api_key=self.api_key, timeout=self.timeout)
        return self._client

    async def classify(self, question: str) -> IntentType:
        try:
            client = self._get_client()
            completion = await client.chat.completions.create(
                model=self.model,
                temperature=0,
                max_tokens=8,
                messages=[
                    {"role": "system", "content": _SYSTEM_PROMPT},
                    {"role": "user", "content": question.strip()},
                ],
            )
            raw = (completion.choices[0].message.content or "").strip().upper()
            # Saca solo la primera palabra por si el modelo agrega ruido
            label = raw.split()[0] if raw else ""
            try:
                return IntentType(label)
            except ValueError:
                logger.warning("Intent no reconocido por IA: %r", raw)
                return IntentType.UNKNOWN
        except OpenAIError as exc:
            logger.warning("OpenAI falló (%s). Se devolverá UNKNOWN.", exc)
            return IntentType.UNKNOWN
        except Exception as exc:  # red, timeout, etc.
            logger.exception("Error inesperado en AIClassifier: %s", exc)
            return IntentType.UNKNOWN