import uuid
from datetime import datetime, timedelta
import os
from jose import jwt
from dotenv import load_dotenv
from app.domain.entities import User
from app.domain.repositories import UserRepository
from app.domain.hashing import HashingService
from app.domain.schemas import TokenResponse, UserResponse

load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))


class RegisterUser:

    def __init__(self, repository: UserRepository, hashing: HashingService):
        self.repository = repository
        self.hashing = hashing

    def execute(self, email: str, password: str, role: str) -> UserResponse:
        existing = self.repository.get_by_email(email)
        if existing:
            raise ValueError("EMAIL_ALREADY_EXISTS")

        hashed = self.hashing.hash(password)
        user = User(
            id=uuid.uuid4(),
            email=email,
            hashed_password=hashed,
            role=role,
            is_active=True,
            created_at=datetime.utcnow(),
        )
        saved = self.repository.save(user)
        return UserResponse(user_id=saved.id, email=saved.email, role=saved.role)


class LoginUser:

    def __init__(self, repository: UserRepository, hashing: HashingService):
        self.repository = repository
        self.hashing = hashing

    def execute(self, email: str, password: str) -> TokenResponse:
        user = self.repository.get_by_email(email)
        if not user:
            raise ValueError("INVALID_CREDENTIALS")

        if not self.hashing.verify(password, user.hashed_password):
            raise ValueError("INVALID_CREDENTIALS")

        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        payload = {
            "user_id": str(user.id),
            "email": user.email,
            "role": user.role,
            "exp": expire,
        }
        token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
        return TokenResponse(
            access_token=token,
            token_type="bearer",
            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )


class GetCurrentUser:

    def __init__(self, repository: UserRepository):
        self.repository = repository

    def execute(self, user_id: uuid.UUID) -> UserResponse:
        user = self.repository.get_by_id(user_id)
        if not user:
            raise ValueError("USER_NOT_FOUND")
        return UserResponse(user_id=user.id, email=user.email, role=user.role)
