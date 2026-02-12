
# Phase 1.1: Core Repair - Stabilization Plan
**Classification**: Security + Data Integrity Patch
**Severity**: CRITICAL (Kernel Modification Required)
**Target**: `spine.db.models.Email`, `spine.chapters.intelligence.processor`

## 1. The Invariant (Governance)
**Tenant Isolation Invariant**:
> For every persistent model that represents tenant-scoped data:
> 1. All read/write operations MUST include `tenant_id` in their predicate.
> 2. No global uniqueness constraint may exist without tenant scoping.

## 2. Migration Strategy (Safe Path)
We will **NOT** use a direct breaking migration. We will use a **Protect-Expand-Contract** strategy.

### Stage 1: Expand (Non-Breaking)
1.  Add `tenant_id` column to `emails` table as `Nullable`.
2.  Deploy Schema.
3.  **Backfill**: Run script to derive `tenant_id` from related `WorkItem` or `User` owner.
    -   *Fallback*: If no relation found, assign to a "Lost & Found" Tenant or default.
4.  **Validate**: Ensure `tenant_id` is populated for 100% of rows.

### Stage 2: Logic Swap
1.  Update `IntelligenceProcessor` to use `tenant_id` in deduplication logic.
2.  Update `EmailRepository` to enforce `tenant_id` filter on all reads.

### Stage 3: Constrain (Lock)
1.  Alter `tenant_id` to `NOT NULL`.
2.  Add Composite Unique Constraint: `UNIQUE (tenant_id, provider_message_id)`.
    -   *Note*: This allows the SAME `provider_message_id` to exist multiple times, provided `tenant_id` is different.

## 3. Execution Protocol
-   **Step 1: Write Failing Test**
    -   Create `tests/test_tenant_isolation.py`.
    -   Scenario: Tenant A has Email X. Tenant B receives Email X.
    -   Expectation: Tenant B *should* get a WorkItem.
    -   Current Reality: Test FAILS (Tenant B gets nothing).
-   **Step 2: Schema Migration (Expand)**
    -   Alembic Revision: Add nullable column.
-   **Step 3: Backfill Data**
    -   Script: `scripts/backfill_tenant_ids.py`.
-   **Step 4: Update Logic**
    -   Modify `processor.py`.
-   **Step 5: Fix Regressions**
    -   Address `test_repository.py` and other failures caused by the change.
-   **Step 6: Schema Migration (Constrain)**
    -   Alembic Revision: Add Constraints.
-   **Step 7: Final verification**
    -   Run Full Regression Suite.

## 4. Risks & Mitigations
-   **Risk**: Idempotency failure creates duplicate WorkItems during backfill.
    -   *Mitigation*: Backfill script must check for existing `tenant_id` before writing.
-   **Risk**: Repository tests fail due to session handling.
    -   *Mitigation*: Audit `conftest.py` and ensure session isolation.
