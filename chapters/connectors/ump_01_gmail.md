
# UMP-CORE-0001: Gmail Connector

**Module**: `chapters.connectors.gmail`
**Type**: **Migration** (Refactoring `spine.core` logic)
**Phase**: Phase 1 (Core Migration)
**Mandate**: `EXEC_MIN_SAAS_V1`

## 1. Objective
Implement a robust Gmail Connector that acts as the "Entry" and "Exit" point for the Vertical Slice.
It must:
1.  **Ingest**: Fetch emails from Gmail API (Transiently).
2.  **Publish**: Emit `EmailIngested` events to the Foundation Bus.
3.  **Send**: Execute send commands via Gmail API.

## 2. Architecture
*   **Client (`client.py`)**: Low-level wrapper around `google-api-python-client`. Handles Auth refreshing.
*   **Service (`service.py`)**: Business logic. Polling, Event Emission, Send Orchestration.

## 3. Implementation Plan
1.  **Create** `chapters/connectors/gmail/client.py`.
2.  **Create** `chapters/connectors/gmail/service.py`.
3.  **Test** `chapters/connectors/tests/test_gmail.py`.

## 4. Verification
*   **Unit Tests**: Mocked Google API calls. Verify Event Emission.

## 5. Definition of Done
*   [ ] Modules created.
*   [ ] 100% Test Coverage.
*   [ ] Verified via Mocked Tests.
