
# Current Data Model Baseline (v0.6)
**Status**: FROZEN

## 1. Identity & Tenancy (`chapters/admin`)
### `Organization`
-   `id`: UUID (PK)
-   `name`: String
-   `tenants`: List[Tenant]

### `Tenant`
-   `id`: UUID (PK)
-   `organization_id`: UUID (FK)
-   `name`: String
-   `tier`: Enum (SOLO, PRO, BUSINESS, ENTERPRISE)
-   `status`: Enum (ACTIVE, SUSPENDED, ARCHIVED)

### `User`
-   `id`: UUID (PK)
-   `email`: String (Unique)
-   `tenant_id`: UUID (FK)
-   `role`: String ("USER", "ADMIN")
-   `status`: String ("ACTIVE")
-   **Note**: `hashed_password` present but commented out/mocked in some flows.

### `AdminUser`
-   `id`: UUID (PK)
-   `email`: String
-   `role`: String ("admin")

## 2. Human-in-the-Loop (`chapters/hitl`)
### `HitlRequest`
-   `id`: String (PK)
-   `tenant_id`: String
-   `work_item_id`: String
-   `reason`: String
-   `context_json`: String (JSON)
-   `state`: Enum (PENDING, CLAIMED, RESOLVED)
-   `claimed_by`: Optional[String]

### `HitlDecision`
-   `id`: String (PK)
-   `request_id`: String (FK)
-   `outcome`: Enum
-   `modified_draft`: String

## 3. Operations
### `LedgerEntry`
-   `id`: Int (PK)
-   `tenant_id`: String
-   `amount`: Int (cents)
-   `stripe_charge_id`: String

## 4. Key Relationships
-   **Strict Hierarchy**: Org -> Tenant -> User.
-   **Loose Coupling**: `HitlRequest` links to `WorkItem` via string ID (Soft Link), likely to avoid circular imports or strict FK constraints across modules.

## 5. Migration Risks
-   `User` table has `hashed_password` commented out in `auth.py` logic.
-   `SystemFlag` uses Key/Value storage for likely config flags.
