
# Current Architecture Baseline (v0.6-pre-gap-fix)
**Generated**: 2026-02-12
**Status**: FROZEN

## 1. High-Level Architecture
The system follows a modular Monolith structure ("Spine") with a React Frontend ("Face").

### Core Modules (`spine/chapters`)
1.  **Public Gateway (`chapters/public`)**:
    -   Handles unauthenticated access.
    -   `auth.py`: Signup flow (Tenant + User creation).
    -   **Gap**: No Login endpoint visible in public router (likely in `api/v1/auth`).

2.  **Admin (`chapters/admin`)**:
    -   Tenant/User management.
    -   `models.py`: Defines `Organization`, `Tenant`, `User`, `LedgerEntry`.
    -   **Constraint**: Multi-tenant by design (Tenant -> User).

3.  **HITL (`chapters/hitl`)**:
    -   Human-in-the-Loop workflows.
    -   `models.py`: `HitlRequest`, `HitlDecision`.
    -   **State Machine**: `HitlState` (Enum).

4.  **Intelligence (`chapters/intelligence`)**:
    -   AI Logic.
    -   Components: `processor`, `proxy`, `streamer`, `triage`.
    -   **Status**: Likely contains the "Zero Storage" logic.

5.  **API Backbone (`api/v1`)**:
    -   Aggregates routers.
    -   `endpoints`: `users`, `auth`, `work_items`, `emails`, `intelligence`, `mind`.

## 2. Infrastructure Assumptions
1.  **Database**: Postgres (SQLModel/SQLAlchemy).
2.  **Auth**: JWT (implied by `config.py` settings).
3.  **LLM**: Gemini / OpenAI (Keys in `config.py`).
4.  **Hosting**: Docker/FastAPI (implied by `main.py`).

## 3. Cross-Cutting Concerns
-   **Config**: `spine/core/config.py` (Pydantic Settings).
-   **Logging**: Basic middleware logging in `main.py`.
-   **CORS**: Allow-all (Dev mode).

## 4. Protected Core List
The following paths are considered **KERNEL** logic and must not be modified without a Refactor Ticket:
-   `spine/core/*`
-   `spine/chapters/admin/models.py` (Auth/Tenant Schema)
-   `spine/chapters/hitl/models.py` (HITL Schema)
-   `spine/main.py` (Boot sequence)
