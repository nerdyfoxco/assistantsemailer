
# UMP-FOUNDATION-0005: Value Objects

**Module**: `foundation.vo`
**Type**: **New Capability**
**Phase**: Phase 0 (Foundation)
**Depends On**: `pydantic`

## 1. Objective
Eliminate "Primitive Obsession" by replacing raw strings and floats with rich Value Objects. This ensures invalid states (e.g., malformed email, negative price) are impossible to represent in the domain layer.

## 2. Proposed Interface

### A. EmailAddress (`foundation.vo.email`)
```python
from pydantic import BaseModel, EmailStr, field_validator

class EmailAddress(BaseModel):
    address: str # Normalized (lowercase)
    name: str | None = None

    @field_validator("address")
    def validate_and_lower(cls, v):
        # Basic validation + lowercase
        if "@" not in v: raise ValueError("Invalid email")
        return v.lower().strip()
    
    def __str__(self):
        if self.name:
            return f"{self.name} <{self.address}>"
        return self.address
```

### B. Money (`foundation.vo.finance`)
```python
from decimal import Decimal
from enum import StrEnum

class Currency(StrEnum):
    USD = "USD"
    EUR = "EUR"

class Money(BaseModel):
    amount: Decimal
    currency: Currency = Currency.USD

    def __add__(self, other):
        if self.currency != other.currency: raise ValueError("Currency mismatch")
        return Money(amount=self.amount + other.amount, currency=self.currency)
```

## 3. Implementation Plan
1.  **Create** `foundation/vo/email.py`.
2.  **Create** `foundation/vo/finance.py`.
3.  **Test** `foundation/tests/test_vo.py`.

## 4. Verification
*   **Unit Test**: Verify validation logic and normalization.
*   **Invariant**: Emails are always lowercase.

## 5. Definition of Done
*   [ ] Modules created.
*   [ ] 100% Test Coverage.
