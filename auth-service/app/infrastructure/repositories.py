import uuid
from typing import Optional
from sqlalchemy.orm import Session
from app.domain.entities import User
from app.domain.repositories import UserRepository
from app.infrastructure.models import UserModel


class UserRepositoryPostgres(UserRepository):

    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> Optional[User]:
        model = self.db.query(UserModel).filter(UserModel.email == email).first()
        if not model:
            return None
        return self._to_entity(model)

    def save(self, user: User) -> User:
        model = UserModel(
            id=user.id,
            email=user.email,
            hashed_password=user.hashed_password,
            role=user.role,
            is_active=user.is_active,
            created_at=user.created_at,
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return self._to_entity(model)

    def get_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        model = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if not model:
            return None
        return self._to_entity(model)

    def _to_entity(self, model: UserModel) -> User:
        return User(
            id=model.id,
            email=model.email,
            hashed_password=model.hashed_password,
            role=model.role,
            is_active=model.is_active,
            created_at=model.created_at,
        )
