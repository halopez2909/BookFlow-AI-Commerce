"""
Entidades del dominio. Son objetos puros de Python, sin dependencias
de SQLAlchemy ni FastAPI: representan los conceptos del negocio.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import uuid4

from app.domain.intents import IntentType


@dataclass
class AssistantInteraction:
    """
    Una interacción del usuario con el asistente: la pregunta, la
    intención detectada y la respuesta generada. Se persiste en
    assistant_db para construir el historial por sesión.
    """
    session_id: str
    user_question: str
    interpreted_intent: IntentType
    answer_text: str
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class BookSnapshot:
    """
    Vista mínima de un libro tal como la consumen el ResponseBuilder y
    los clients. Cada client (Catalog/Inventory/Pricing) llena los
    campos que le competen y deja el resto en None.
    """
    book_id: str
    title: Optional[str] = None
    author: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    available: Optional[bool] = None
    stock: Optional[int] = None
    price: Optional[float] = None
    currency: Optional[str] = None