from typing import Optional, Tuple
from sqlalchemy.orm import Session


class DuplicateDetector:
    def __init__(self, catalog_db: Session):
        self.catalog_db = catalog_db

    def detect(self, isbn: Optional[str]) -> Tuple[bool, Optional[str]]:
        if not isbn:
            return False, None
        try:
            from sqlalchemy import text
            result = self.catalog_db.execute(
                text("SELECT id FROM books WHERE isbn = :isbn LIMIT 1"),
                {"isbn": isbn}
            ).fetchone()
            if result:
                return True, str(result[0])
            return False, None
        except Exception:
            return False, None
