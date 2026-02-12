
# UMP-FOUNDATION-0001: Authority System

**Module**: `foundation.authority`
**Type**: **New Capability**
**Phase**: Phase 0 (Foundation)
**Depends On**: None

## 1. Objective
Establish the **Execution Authority** mechanism to strictly govern which system (Legacy `spine` or Canonical `foundation`) owns a specific logic path or data entity at runtime. This is the core enforcer of the Strangler Pattern.

## 2. Proposed Interface

### A. Enums (`foundation.common.types`)
```python
from enum import StrEnum, auto

class ExecutionAuthority(StrEnum):
    LEGACY = auto()      # Old system owns it (Default)
    CANONICAL = auto()   # New system owns it
    DUAL = auto()        # Both run (Shadow mode), Canonical result ignored/logged
    DISABLED = auto()    # Feature turned off
```

### B. Policy Contract (`foundation.authority.policy`)
```python
class AuthorityPolicy(BaseModel):
    feature_id: str
    authority: ExecutionAuthority
    rollout_percentage: int = 0
    allow_tenants: list[str] = Field(default_factory=list)

    def resolve(self, context: dict) -> ExecutionAuthority:
        # Logic to determine authority based on context (tenant, random, etc.)
        ...
```

### C. Registry (`foundation.authority.registry`)
*   Hardcoded defaults (Code-as-Config) for Phase 0.
*   Future: DB-backed.

## 3. Implementation Plan
1.  **Create** `foundation/common/types.py` (Enums).
2.  **Create** `foundation/authority/policy.py` (Logic).
3.  **Create** `foundation/authority/registry.py` (Config).
4.  **Test** `foundation/tests/test_authority.py`.

## 4. Verification
*   **Unit Test**: Ensure `resolve()` returns correct Enum based on inputs.
*   **Invariant**: Default must ALWAYS be `LEGACY` for now.

## 5. Definition of Done
*   [ ] Modules created.
*   [ ] 100% Test Coverage.
*   [ ] Exposed via `foundation` package.
