
# Strangler Boundary Definition (Phase 0)

**Objective**: Explicitly define the operational boundary between **Legacy (`spine/`)** and **Canonical (`foundation/`)** systems to prevent "Undefined Behavior" and "Data Corruption".

## 1. Database Ownership Model

| Question | Answer | Rule |
| :--- | :--- | :--- |
| **Does Foundation own new tables?** | **YES** | `foundation/` will introduce *new* tables (e.g., `feature_flags`, `canonical_audit_log`, `inventory_ledger`) in the `public` schema (or a new `foundation` schema if supported). |
| **Can Foundation write to Legacy tables?** | **NO** | `foundation/` code must **NEVER** write directly to `emails`, `users`, or `work_items` tables owned by `spine`. |
| **Who owns the `Email` entity?** | **Spine (Legacy)** | For Phase 0 and Phase 1, `spine` retains full ownership of the `Email` lifecycle. Foundation may *read* via replicas or defined interfaces, but never write. |
| **How is shared state managed?** | **Interface-Only** | If Foundation needs to know about a User, it must query a read-only View or use the `spine` API. |

## 2. API & Routing Boundary

| Component | Responsibility | Implementation |
| :--- | :--- | :--- |
| **Ingress Router** | Traffic Switching | A dedicated **API Gateway** (or standard FastAPI `APIRouter` mounting) will act as the Switch. |
| **Traffic Split** | **Path-Based** | `api/v1/*` -> `spine` (Legacy)<br>`api/v2/foundation/*` -> `foundation` (New) |
| **Feature Flags** | Safe Rollout | We will use a simple DB-backed Feature Flag system (`foundation.toggles`) to control code paths within `spine` if necessary. |
| **Rollback** | **Instant** | If `foundation` fails, we disable the Feature Flag or revert the Ingress Route. |

## 3. Dependency Direction

*   ❌ `foundation` -> depends on -> `spine` (FORBIDDEN)
*   ✅ `spine` -> depends on -> `foundation` (ALLOWED - e.g., Spine uses Foundation's Audit Log)
*   ✅ `foundation` -> depends on -> `libraries` (ALLOWED - e.g., Pydantic, SQLAlchemy)

## 4. Execution Authority
*   **Legacy (`spine`)**: Continues to run automations based on existing logic.
*   **Canonical (`foundation`)**: Initially **Passive**. It will observe and log (Audit) but not act until explicitly authorized by the **Authority Contract** (Phase 0).

**Signed**,
*Canonical UMP Architect*
