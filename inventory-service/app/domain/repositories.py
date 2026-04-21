from abc import ABC, abstractmethod
from typing import Optional, List
import uuid
from app.domain.entities import InventoryItem, ImportBatch, ImportError


class InventoryRepository(ABC):

    @abstractmethod
    def save(self, item: InventoryItem) -> InventoryItem:
        pass

    @abstractmethod
    def get_by_id(self, item_id: uuid.UUID) -> Optional[InventoryItem]:
        pass

    @abstractmethod
    def get_by_batch(self, batch_id: uuid.UUID) -> List[InventoryItem]:
        pass


class ImportBatchRepository(ABC):

    @abstractmethod
    def save(self, batch: ImportBatch) -> ImportBatch:
        pass

    @abstractmethod
    def get_by_id(self, batch_id: uuid.UUID) -> Optional[ImportBatch]:
        pass

    @abstractmethod
    def get_all(self, page: int, page_size: int) -> tuple[List[ImportBatch], int]:
        pass

    @abstractmethod
    def update(self, batch: ImportBatch) -> ImportBatch:
        pass


class ImportErrorRepository(ABC):

    @abstractmethod
    def save(self, error: ImportError) -> ImportError:
        pass

    @abstractmethod
    def get_by_batch(self, batch_id: uuid.UUID, error_type: Optional[str]) -> List[ImportError]:
        pass
