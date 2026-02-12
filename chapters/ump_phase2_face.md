
# Phase 2: Frontend (The Face)

**Mandate**: `EXEC_MIN_SAAS_V1`
**Goal**: provide a usable UI for the Vertical Slice (Inbox -> Draft -> Approve).
**Stack**: Vite + React + TypeScript + TailwindCSS + Shadcn/UI (simplified).

## 1. UMP-FACE-0001: Initialization
*   **Goal**: Setup `face/` directory with a working Vite app.
*   **Actions**:
    *   `npm create vite@latest face -- --template react-ts`
    *   Install TailwindCSS.
    *   Setup Proxy to Backend (`localhost:8000`).

## 2. UMP-FACE-0002: API Client & State
*   **Goal**: Typed client for `chapters/api`.
*   **Files**:
    *   `face/src/lib/api.ts`: Fetch wrapper.
    *   `face/src/lib/types.ts`: TypeScript interfaces for `WorkItem`.

## 3. UMP-FACE-0003: Inbox View
*   **Goal**: List `WorkItems` in `NEW` or `REVIEW` state.
*   **UI**: Simple Table or List Card.
*   **Interaction**: Click to select Item.

## 4. UMP-FACE-0004: Draft Action View
*   **Goal**: Display the AI Draft and allow "Approve".
*   **UI**: Split view (Original Snippet vs AI Draft).
*   **Actions**: "Generate Draft" (if NEW), "Approve" (if REVIEW).

## 5. Verification
*   **Manual**: Run `npm run dev`, open browser, perform the loop.
*   **Artifact**: Screenshot of the UI in action.
