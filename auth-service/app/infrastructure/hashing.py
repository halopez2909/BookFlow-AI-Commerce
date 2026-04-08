from passlib.context import CryptContext
from app.domain.hashing import HashingService


class BCryptHashingService(HashingService):

    def __init__(self):
        self.context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12)

    def hash(self, plain: str) -> str:
        return self.context.hash(plain)

    def verify(self, plain: str, hashed: str) -> bool:
        return self.context.verify(plain, hashed)
