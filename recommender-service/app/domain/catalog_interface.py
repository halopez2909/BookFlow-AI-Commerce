from abc import ABC, abstractmethod
from typing import List, Dict, Any

class CatalogServiceInterface(ABC):
    
    @abstractmethod
    async def get_books_by_ids(self, book_ids: List[int]) -> List[Dict[str, Any]]:
        """Obtiene los detalles de una lista de libros desde el servicio de catálogo."""
        pass