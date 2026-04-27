from typing import Optional, List
from app.domain.entities import Condition


class ValidationResult:
    def __init__(self, is_valid: bool, error_type: Optional[str] = None, message: Optional[str] = None):
        self.is_valid = is_valid
        self.error_type = error_type
        self.message = message


class BaseValidator:
    def __init__(self):
        self._next: Optional[BaseValidator] = None

    def set_next(self, validator: "BaseValidator") -> "BaseValidator":
        self._next = validator
        return validator

    def validate(self, row: dict) -> Optional[ValidationResult]:
        if self._next:
            return self._next.validate(row)
        return None


class RequiredFieldsValidator(BaseValidator):
    REQUIRED_FIELDS = ["external_code", "book_reference", "quantity_available", "condition"]

    def validate(self, row: dict) -> Optional[ValidationResult]:
        for field in self.REQUIRED_FIELDS:
            if not row.get(field):
                return ValidationResult(
                    is_valid=False,
                    error_type="missing_field",
                    message=f"Required field '{field}' is missing or empty",
                )
        return super().validate(row)


class ConditionValidator(BaseValidator):
    VALID_CONDITIONS = [c.value for c in Condition]

    def validate(self, row: dict) -> Optional[ValidationResult]:
        condition = row.get("condition", "")
        if condition not in self.VALID_CONDITIONS:
            return ValidationResult(
                is_valid=False,
                error_type="invalid_condition",
                message=f"Condition '{condition}' is not valid. Must be one of: {', '.join(self.VALID_CONDITIONS)}",
            )
        return super().validate(row)


class DefectsValidator(BaseValidator):
    WORN_OR_DAMAGED = [Condition.WORN.value, Condition.DAMAGED.value]

    def validate(self, row: dict) -> Optional[ValidationResult]:
        condition = row.get("condition", "")
        defects = row.get("defects", "")
        if condition in self.WORN_OR_DAMAGED and not defects:
            return ValidationResult(
                is_valid=False,
                error_type="missing_defects",
                message=f"Field 'defects' is required when condition is '{condition}'",
            )
        return super().validate(row)


def build_validator_chain() -> BaseValidator:
    required = RequiredFieldsValidator()
    condition = ConditionValidator()
    defects = DefectsValidator()
    required.set_next(condition).set_next(defects)
    return required
