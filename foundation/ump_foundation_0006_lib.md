
# UMP-FOUNDATION-0006: Core Utilities

**Module**: `foundation.lib`
**Type**: **New Capability**
**Phase**: Phase 0 (Foundation)
**Depends On**: `passlib`, `logging`

## 1. Objective
Provide standardized, safe wrappers for common cross-cutting concerns: **Structured Logging** and **Security Primitives** (Hashing). This removes direct dependencies on `spine.core` and ensures consistent behavior across the Canonical system.

## 2. Proposed Interface

### A. Structured Logger (`foundation.lib.logging`)
```python
import logging
from typing import Any

class StructuredLogger:
    def info(self, msg: str, **kwargs): ...
    def error(self, msg: str, exc_info=True, **kwargs): ...
    
    # Factory
    @staticmethod
    def get_logger(name: str) -> 'StructuredLogger': ...
```

### B. Security (`foundation.lib.security`)
```python
class PasswordManager:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool: ...
    
    @staticmethod
    def get_password_hash(password: str) -> str: ...
```

## 3. Implementation Plan
1.  **Create** `foundation/lib/logging.py`.
2.  **Create** `foundation/lib/security.py`.
3.  **Test** `foundation/tests/test_lib.py`.

## 4. Verification
*   **Unit Test**: Verify hashing consistency. verify logger output format (mocked).

## 5. Definition of Done
*   [ ] Modules created.
*   [ ] 100% Test Coverage.
