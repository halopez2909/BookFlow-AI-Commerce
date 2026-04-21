from app.domain.validators import build_validator_chain


def test_valid_row():
    validator = build_validator_chain()
    row = {
        "external_code": "EXT001",
        "book_reference": "REF001",
        "quantity_available": "5",
        "condition": "new",
        "defects": "",
    }
    result = validator.validate(row)
    assert result is None


def test_missing_required_field():
    validator = build_validator_chain()
    row = {
        "external_code": "",
        "book_reference": "REF001",
        "quantity_available": "5",
        "condition": "new",
    }
    result = validator.validate(row)
    assert result is not None
    assert not result.is_valid
    assert result.error_type == "missing_field"


def test_invalid_condition():
    validator = build_validator_chain()
    row = {
        "external_code": "EXT001",
        "book_reference": "REF001",
        "quantity_available": "5",
        "condition": "broken",
    }
    result = validator.validate(row)
    assert result is not None
    assert not result.is_valid
    assert result.error_type == "invalid_condition"


def test_worn_without_defects():
    validator = build_validator_chain()
    row = {
        "external_code": "EXT001",
        "book_reference": "REF001",
        "quantity_available": "5",
        "condition": "worn",
        "defects": "",
    }
    result = validator.validate(row)
    assert result is not None
    assert not result.is_valid
    assert result.error_type == "missing_defects"
