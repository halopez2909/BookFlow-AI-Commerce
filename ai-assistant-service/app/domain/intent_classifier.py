"""
Interfaz Strategy para clasificar la intención de la pregunta del
usuario. Las implementaciones concretas viven en
app/infrastructure/providers/.
"""
from abc import ABC, abstractmethod

from app.domain.intents import IntentType


class IntentClassifier(ABC):
    """Contrato del patrón Strategy: dado un texto, devuelve un IntentType."""

    @abstractmethod
    async def classify(self, question: str) -> IntentType:
        """
        Clasifica la pregunta en una de las IntentType definidas.

        Debe ser tolerante a fallos: si no puede clasificar con
        certeza, retorna IntentType.UNKNOWN (Null Object Pattern).
        NUNCA debe lanzar excepción al caller.
        """
        raise NotImplementedError