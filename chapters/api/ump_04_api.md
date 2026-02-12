
# UMP-CORE-0004: API & UI

**Module**: `chapters.api`
**Type**: **New Capability**
**Phase**: Phase 1 (Core Migration)
**Mandate**: `EXEC_MIN_SAAS_V1`

## 1. Objective
Expose the Vertical Slice to the outside world (Frontend/Swagger).
It must allow:
1.  **Listing**: See emails needing attention.
2.  **Viewing**: See the AI-generated draft.
3.  **Actioning**: Approve the draft (triggering Send).

## 2. Architecture
*   **Router (`router.py`)**: FastAPI APIRouter definition.
*   **Dependencies (`deps.py`)**: Singleton implementations of `WorkManager`, `GmailService`, `BrainService`.
*   **Schema**: Pydantic models for Responses.

## 3. Endpoints
*   `GET /api/v2/work-items`: List all items.
*   `GET /api/v2/work-items/{item_id}`: Get specific item.
*   `POST /api/v2/work-items/{item_id}/approve`: Transition to `SENDING`.

## 4. Implementation Plan
1.  **Create** `chapters/api/deps.py` (Wiring).
2.  **Create** `chapters/api/router.py`.
3.  **Test** `chapters/api/tests/test_api.py`.

## 5. Definition of Done
*   [ ] API Router created.
*   [ ] Endpoints verified via TestClient.
