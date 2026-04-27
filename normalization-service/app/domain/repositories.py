from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities import NormalizedRecord


class NormalizedRecordRepository(ABC):
    @abstractmethod
    def save(self, record: NormalizedRecord) -> NormalizedRecord:
        pass

    @abstractmethod
    def find_all(self) -> List[NormalizedRecord]:
        pass

    @abstractmethod
    def find_by_id(self, record_id: str) -> Optional[NormalizedRecord]:
        pass
