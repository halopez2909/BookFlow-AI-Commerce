from typing import List, Optional
from datetime import datetime

class Recommendation:
    def __init__(
        self, 
        id: Optional[int], 
        user_id: str, 
        recommended_books: List[int], 
        reason: str, 
        created_at: Optional[datetime] = None
    ):
        self.id = id
        self.user_id = user_id
        self.recommended_books = recommended_books  # Lista de IDs de los libros sugeridos
        self.reason = reason                        # Por qué se le recomienda (ej: "Basado en tu historial")
        self.created_at = created_at or datetime.utcnow()

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "recommended_books": self.recommended_books,
            "reason": self.reason,
            "created_at": self.created_at.isoformat()
        }