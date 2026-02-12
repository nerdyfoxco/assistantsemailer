
# Phase 1: Core Migration (Vertical Slice v0)

**Mandate**: `EXEC_MIN_SAAS_V1`
**Goal**: Deploy `VS_EMAIL_REPLY_CORE` (User -> Inbox -> Decision -> Draft -> Approval -> Send -> Close).
**Strategy**: Strangler Fig Pattern. New `chapters` modules will take over specific responsibilities from `spine`.

## 1. UMP-CORE-0001: Connector Layer (Gmail)
*   **Goal**: Ingest emails and Send emails via Gmail API.
*   **Input**: Gmail API credentials (from `foundation.auth`).
*   **Output**: `EmailIngested` event (to Bus), Sent Email via API.
*   **Files**: `chapters/connectors/gmail/client.py`, `chapters/connectors/gmail/service.py`.

## 2. UMP-CORE-0002: Work Engine
*   **Goal**: Manage the lifecycle of an Email Reply.
*   **Input**: `EmailIngested` event.
*   **State Machine**: `New` -> `Drafting` -> `Review` -> `Sending` -> `Closed`.
*   **Files**: `chapters/work/item.py`, `chapters/work/manager.py`.

## 3. UMP-CORE-0003: Brain (Drafting)
*   **Goal**: Generate a draft reply using LLM (Shared Pattern).
*   **Input**: `WorkItemCreated` event.
*   **Logic**: `Input -> Template -> LLM -> Draft`.
*   **Files**: `chapters/brain/processor.py`, `chapters/brain/prompts.py`.

## 4. UMP-CORE-0004: API & UI Support
*   **Goal**: Allow user to View and Approve drafts.
*   **Endpoints**:
    *   `GET /api/v2/work-items` (List)
    *   `GET /api/v2/work-items/{id}` (Detail)
    *   `POST /api/v2/work-items/{id}/approve` (Action)
*   **Files**: `chapters/api/router.py`.

## 5. Verification
*   **Visual**: Swagger UI check of new V2 endpoints.
*   **Smoke**: Simulate full flow via Test Client.
