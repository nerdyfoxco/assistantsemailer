
# UMP-FOUNDATION-0007: Testing Primitives

**Module**: `foundation.testing`
**Type**: **New Capability**
**Phase**: Phase 0 (Foundation)
**Depends On**: `pytest`

## 1. Objective
Standardize testing patterns across the Canonical architecture. Provide a central location for test markers, common fixtures, and utilities to prevent copy-paste in individual module test suites.

## 2. Proposed Interface

### A. Markers (`foundation.testing.markers`)
```python
import pytest

# Standard markers to classify test speed/scope
unit = pytest.mark.unit
integration = pytest.mark.integration
e2e = pytest.mark.e2e
slow = pytest.mark.slow
```

### B. Fixtures (`foundation.testing.fixtures`)
*   `foundation_config`: Returns a clean `GlobalSettings` instance.
*   `in_memory_bus`: Returns a fresh `InMemoryEventBus`.

## 3. Implementation Plan
1.  **Create** `foundation/testing/markers.py`.
2.  **Create** `foundation/testing/fixtures.py`.
3.  **Test** `foundation/tests/test_testing_primitives.py`.

## 4. Verification
*   **Unit Test**: Verify markers can be applied. Verify fixtures return expected objects.

## 5. Definition of Done
*   [ ] Modules created.
*   [ ] 100% Test Coverage.
