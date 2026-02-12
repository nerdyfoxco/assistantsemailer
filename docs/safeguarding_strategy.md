
# Safeguarding Strategy: The "Strangler Fig" Protocol

**Objective**: Guarantee that **Current Functionality** (Sealed UMPs in `inventory.md`) is **NEVER compromised** while building the new **Canonical Architecture**.

---

## 1. The Core Rule: "Add Only, Never Delete"
Until a new **Chapter** is fully **Sealed** and **Verified**, the corresponding **Legacy Code** in `spine/` or `face/` is **Immutable**.

*   **Legacy**: `spine/chapters/*` (Python Monolith), `face/src/chapters/*` (React Features).
*   **Canonical**: `foundation/`, `chapters/brain/`, `chapters/hands/`, etc. (New Structure).

**Protocol**:
1.  **Build New**: Implement `chapters/<organ>/<topic>` in the new folder.
2.  **Verify New**: Run unit/contract tests for the new module.
3.  **Parity Check**: Confirm new module matches or exceeds old module functionality.
4.  **Switch Traffic**: Update routing (API/UI) to point to the New Module.
5.  **Monitor**: Watch for regressions.
6.  **Deprecate Old**: Only *then* mark the old code as "Deprecated" (do not delete yet).
7.  **Archive**: Delete old code only after a "Cooling Period" (e.g., 1 Sprint).

---

## 2. Inventory Protection
The `inventory.md` file is the **Source of Truth** for what "Works".
*   **Rule**: I cannot modify a "Sealed" line in `inventory.md` unless I am explicitly executing a **Migration UMP** that replaces it.
*   **Enforcement**: The **Authority Contract** (Phase 0) will include a check: "If UMP targets a Legacy Feature, it must declare a `replacement_strategy`."

---

## 3. Test Harness as the "Safety Net"
We have a suite of tests that verify the *current* system:
*   `tests/test_tenant_isolation.py` (Critical Security)
*   `spine/tests/*` (Domain Logic)
*   `face/src/**/*.test.tsx` (UI Logic)

**Rule**:
*   These tests **MUST PASS** at every single Task Boundary.
*   We will **NOT** refactor these tests to fit the new system immediately. They serve as the "Anchor" to ensure we haven't broken the old system.
*   New system will have *new* tests in `chapters/<organ>/test/`.

---

## 4. Specific Asset Protection

| Asset | Migration Strategy | Protection Mechanism |
| :--- | :--- | :--- |
| **Tenant Data** (DB) | **Zero-Migration** (initially) | New modules will connect to the *existing* DB schema first. We will use the existing `models.py` as a shared library or duplicate the models strictly to avoid schema breaks. |
| **UI** (`face/`) | **Parallel Mount** | New UI components will be built in `face/src/canonical/` or similar. We will mount them side-by-side with old components using Feature Flags. |
| **Logic** (`spine/`) | **Import Aliasing** | New modules may *import* from `spine/` temporarily to reuse logic (e.g., helpers), but `spine/` will never import from `chapters/` (Unidirectional Dependency). |

---

## 5. Rollback Capability
If a "Switch Traffic" step fails:
*   **Revert Routing**: Point API/UI back to the Legacy Module.
*   **Disable Feature Flag**: Turn off the new UI.
*   **Data Integrity**: Since we share the DB (initially), data written by the new module must be compatible with the old module (Backward Compatibility Rule).

## 6. Execution Authority Guard
The **Phase 0: Authority Contract** will enforce this:
*   AI cannot `rm -rf` logic folders.
*   AI cannot `DROP TABLE` without explicit user override.
*   AI cannot Overwrite `inventory.md` sealed items without a "Successor Link".

---

**Signed**,
*Canonical UMP Architect*
