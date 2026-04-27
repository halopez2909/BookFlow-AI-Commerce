from abc import ABC, abstractmethod
from typing import List


class FileParser(ABC):

    @abstractmethod
    def parse(self, file_bytes: bytes) -> List[dict]:
        pass
