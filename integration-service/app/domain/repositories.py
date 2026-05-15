from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.entities import IntegrationFlow


class IntegrationFlowRepository(ABC):
    @abstractmethod
    def save(self, flow: IntegrationFlow) -> IntegrationFlow:
        pass

    @abstractmethod
    def find_by_id(self, flow_id: str) -> Optional[IntegrationFlow]:
        pass

    @abstractmethod
    def find_by_batch_id(self, batch_id: str) -> Optional[IntegrationFlow]:
        pass

    @abstractmethod
    def find_all(self) -> List[IntegrationFlow]:
        pass
