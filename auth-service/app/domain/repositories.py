from abc import ABC, abstractmethod
from typing import Optional
import uuid
from app.domain.entities import User


class UserRepository(ABC):

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    def save(self, user: User) -> User:
        pass

    @abstractmethod
    def get_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        pass
