import uuid
from datetime import datetime


class User:
    def __init__(
        self,
        id: uuid.UUID,
        email: str,
        hashed_password: str,
        role: str,
        is_active: bool,
        created_at: datetime,
    ):
        self.id = id
        self.email = email
        self.hashed_password = hashed_password
        self.role = role
        self.is_active = is_active
        self.created_at = created_at
