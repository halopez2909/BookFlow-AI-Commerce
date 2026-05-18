from app.domain.specifications import EligibilitySpecification
from app.domain.models import Book
def test_specification():
    spec = EligibilitySpecification()
    assert spec is not None
