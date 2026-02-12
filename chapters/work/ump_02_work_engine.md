
# UMP-CORE-0002: Work Engine

**Module**: `chapters.work`
**Type**: **New Capability** (Replaces `spine.core` workflow logic)
**Phase**: Phase 1 (Core Migration)
**Mandate**: `EXEC_MIN_SAAS_V1`

## 1. Objective
Implement the "State Machine" for the Vertical Slice.
It must:
1.  **Consume**: `EmailIngested` events.
2.  **Create**: A `WorkItem` representing the need to reply.
3.  **Manage State**: `NEW` -> `DRAFTING` -> `REVIEW` -> `SENDING` -> `CLOSED`.
4.  **Persistence**: (In-Memory for Phase 1 start, then DB). *Note: We will use a simple Repository interface that can swap to DB later.*

## 2. Architecture
*   **Domain (`item.py`)**: `WorkItem` class with state transitions.
*   **Service (`manager.py`)**: Subscribes to events, orchestrates the flow.

## 3. Implementation Plan
1.  **Create** `chapters/work/item.py` (State Enum + Class).
2.  **Create** `chapters/work/manager.py` (Event Handler).
3.  **Test** `chapters/work/tests/test_work.py`.

## 4. WorkItem Schema (Vertical Slice)
```python
class WorkItemState(Enum):
    NEW = "NEW"
    DRAFTING = "DRAFTING"  # Brain is working
    REVIEW = "REVIEW"      # Waiting for User
    SENDING = "SENDING"    # Handing off to Connector
    CLOSED = "CLOSED"      # Done

class WorkItem:
    id: str
    tenant_id: str
    source_message_id: str
    state: WorkItemState
    draft_context: dict # Stores generated draft
```

## 5. Definition of Done
*   [ ] Modules created.
*   [ ] State Machine Logic Verified.
*   [ ] Event Consumption Verified.
