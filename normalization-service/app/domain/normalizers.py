import re
from abc import ABC, abstractmethod
from typing import Optional
from unidecode import unidecode


class Normalizer(ABC):
    @abstractmethod
    def normalize(self, value: str) -> str:
        pass


class TitleNormalizer(Normalizer):
    def normalize(self, value: str) -> str:
        if not value:
            return value
        cleaned = re.sub(r'\s+', ' ', value.strip())
        cleaned = re.sub(r'[^\w\s\-\'\:\,\.\(\)\!\?]', '', cleaned)
        return cleaned[0].upper() + cleaned[1:].lower() if cleaned else cleaned


class AuthorNormalizer(Normalizer):
    def normalize(self, value: str) -> str:
        if not value:
            return value
        normalized = unidecode(value.strip())
        parts = normalized.split(',')
        if len(parts) == 2:
            return f"{parts[0].strip()}, {parts[1].strip()}"
        parts = normalized.split()
        if len(parts) >= 2:
            last = parts[-1]
            first = ' '.join(parts[:-1])
            return f"{last}, {first}"
        return normalized


class ISBNValidator:
    def validate(self, isbn: Optional[str]) -> bool:
        if not isbn:
            return False
        try:
            from stdnum import isbn as isbn_lib
            return isbn_lib.is_valid(isbn)
        except Exception:
            return False


class ISSNValidator:
    def validate(self, issn: Optional[str]) -> bool:
        if not issn:
            return True
        try:
            from stdnum import issn as issn_lib
            return issn_lib.is_valid(issn)
        except Exception:
            return False
