
# Stabilization Plan: Core Invariant Repair

**Status**: CRITICAL / BLOCKING
**Objective**: Stabilize the `spine` core to 100% correctness before any `foundation` or `chapters` work begins.

## 1. The "Zero-Tolerance" Rule
*   No new features.
*   No architectural refactoring (Canonical).
*   Only **Kernel Repairs**.

## 2. Invariant Checklist (Must Be All Green)
- [ ] **Tenant Isolation**: Data leakage impossible (Constraint + Logic).
- [ ] **Idempotency**: Message processing deduplication works per-tenant.
- [ ] **Repository**: Unit tests pass (no mocked-session leaks).
- [ ] **API Surface**: OpenAPI schema generation is stable and valid.
- [ ] **Imports**: No circular dependencies in `spine`.

## 3. Repair Sequence (Linear)
1.  **Verify Tenant Fix**: Confirm `test_tenant_isolation.py` passes with the Constraint.
2.  **Fix Repository Tests**: Address distinct `db_session` issues in `spine/tests/`.
3.  **Fix API Mismatches**: Ensure `export_openapi.py` runs without error.
4.  **Seal Core**: Tag the git commit as `core-stable-v1`.

## 4. Next Step (Gate)
Only when ALL compliance checks pass -> **Proceed to Phase 0 (Foundation)**.
Until then -> **Stay in Core Repair**.
