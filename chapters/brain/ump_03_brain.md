
# UMP-CORE-0003: Brain / Drafting

**Module**: `chapters.brain`
**Type**: **New Capability**
**Phase**: Phase 1 (Core Migration)
**Mandate**: `EXEC_MIN_SAAS_V1`

## 1. Objective
Implement the "Brain" that generates email drafts.
It must:
1.  **Listen**: For `WorkItemCreated` (or be triggered by Manager).
2.  **Think**: Select a Tone Template (e.g., "Professional", "Casual").
3.  **Generate**: Call LLM to produce a draft.
4.  **Update**: Save draft to `WorkItem` and move state to `REVIEW`.

## 2. Architecture
*   **LLM Interface (`llm.py`)**: Abstract wrapper for AI providers (OpenAI/Gemini/Anthropic).
*   **Prompts (`prompts.py`)**: Jinja2 or f-string templates for drafting.
*   **Service (`service.py`)**: Orchestrator (WorkItem -> Context -> Draft).

## 3. Implementation Plan
1.  **Create** `chapters/brain/llm.py`.
2.  **Create** `chapters/brain/prompts.py`.
3.  **Create** `chapters/brain/service.py`.
4.  **Test** `chapters/brain/tests/test_brain.py`.

## 4. Tone Architecture (Phase 3 Prep)
*   We will use a **Simple Template Strategy** for v0.
*   "Tone" will be a simple string parameter for now.

## 5. Definition of Done
*   [ ] Modules created.
*   [ ] LLM Interface Mocked & Tested.
*   [ ] Draft Generation Loop Verified.
