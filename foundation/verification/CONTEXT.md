# UMP-00-04: Phase 15.H Runtime Engine

## Purpose
To implement the "Continuous Verification" layer. This engine sits *inside* the application and vetoes actions that violate the Deployment Readiness Contract (DRC) at runtime.

## Context
"A runtime engine that checks guarantees on *every* action."
We needed a way to ensure "No Send Without Approval" is not just a policy, but a physical impossibility.

## Requirements
1.  **Guarantees**: defined classes (e.g., `G_Auth`, `G_Data`).
2.  **Verifier Decorator**: `@verify(guarantees=[...])` wrapping sensitive functions.
3.  **Veto Power**: If the guarantee check fails, the function **MUST NOT EXECUTE**.
4.  **Logging**: Failures are audited as Security Events.

## Verification
10-Test Suite (`test_verification.py`):
- Function permitted when conditions met.
- Function blocked when conditions failed.
- Arguments inspected correctly.
- Exception mapping (ValidationFault).
