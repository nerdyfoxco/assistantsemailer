# UMP-00-02: Tenant Isolation Model

## Purpose
To define the fundamental data structures (`Tenant`, `User`) and the logic that validates access. This is the **Security Root**. If this fails, data leaks.

## Context
"Strict tenant isolation."
In v0, we must prove that User A cannot see User B's data *before* we build the database.

## Requirements
1.  **Models**: defined in `models.py`.
2.  **Logic**: `Context` object that carries the current Actor.
3.  **Isolation**: `validate_access(actor, resource)` function.
4.  **No Leaks**: Tests must prove cross-tenant access throws exceptions.

## Verification
10-Test Suite (`test_identity.py`) verifying:
- Tenant creation.
- User assignment.
- Valid access allowed.
- Invalid access (wrong tenant) BLOCKED.
- Role checks (Admin vs Member).
