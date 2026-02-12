
# Phase 3 — Canonical UMP: Authoritative Template + CH-01 Execution

**Objective**: Provide the **Authoritative UMP Template** (E2E) and the full execution specs for **CH-01 (Brain)** to start the migration.

---

## 1. Authoritative UMP Template (Strict)
*Copy this JSON structure for every new UMP. All fields mandatory.*

```json
{
  "ump_id": "UMP-XXXX",
  "chapter_id": "CH-XX",
  "topic_id": "TP-XX",
  "phase_id": "PH-XX",
  "title": "Brief Actionable Title",
  "status": "planned",
  "immutability": {
    "sealed": false,
    "seal_path": "ump/UMP-XXXX/seal.json",
    "successor_policy": "new_ump_required_for_changes"
  },
  "scope": {
    "module_path": "chapters/<organ>/<topic>/",
    "allowed_paths": [
      "chapters/<organ>/<topic>/**"
    ],
    "forbidden_paths": [
      "**/*"
    ],
    "allowed_shared_paths": [
      "foundation/contracts/pipes/** (if needed)"
    ]
  },
  "contracts": {
    "pipes_added_or_modified": [
      {
        "pipe_id": "pipe.<domain>.<action>.v1",
        "direction": "producer|consumer",
        "producer": "chapters/<organ>/<topic>",
        "consumer": "chapters/<organ>/<topic>",
        "schema_path": "foundation/contracts/pipes/schemas/<pipe>.schema.json",
        "version": "1.0.0",
        "compatibility": "strict"
      }
    ]
  },
  "files": [
    {
      "path": "src/index.ts",
      "operation": "create",
      "context": "Entrypoint",
      "purpose": "Initialize service and bind pipes",
      "connectivity": {
        "imports": [],
        "exports": ["main"],
        "pipes_produced": [],
        "pipes_consumed": []
      },
      "build_prompt": "Create a file that...",
      "json_spec_path": "ump/UMP-XXXX/spec.index.ts.json"
    }
  ],
  "build": {
    "commands": ["pnpm build"],
    "expected_artifacts": ["dist/index.js"]
  },
  "tests": {
    "levels": ["unit", "contract"],
    "commands": ["pnpm test"],
    "acceptance_criteria": [
      "Server starts on port 3000",
      "Health check returns 200"
    ]
  },
  "observability": {
    "logging": ["startup", "shutdown", "error"],
    "metrics": ["uptime", "request_count"],
    "tracing": ["handler_span"]
  },
  "security": {
    "data_classification": "internal",
    "validation": ["input_schema_check"],
    "redaction": ["pii_scrub"]
  },
  "risks": [
    {
      "risk": "Port conflict",
      "mitigation": "Use configurable env var PORT"
    }
  ]
}
```

---

## 2. CH-01: Brain (The Strategist) - Execution Specs

### TP-01: topic-orchestration (The Conductor)
**Module Path**: `chapters/brain/topic-orchestration/`

#### UMP-0110: Skeleton & Contracts
**Title**: Create Brain Orchestration Skeleton & Pipe Contracts.
**Scope**: `chapters/brain/topic-orchestration/**`, `foundation/contracts/pipes/**`

**Files to Create**:

1.  `chapters/brain/topic-orchestration/package.json`
    *   **Prompt**: Standard Node.js package. Name `@fyxer/brain-orchestration`. Deps: `zod`, `fastify` (or similar).
2.  `chapters/brain/topic-orchestration/tsconfig.json`
    *   **Prompt**: Strict TS config, extending `../../../tsconfig.base.json`.
3.  `foundation/contracts/pipes/schemas/pipe.workflow.event.v1.schema.json`
    *   **Prompt**: JSON Schema 7. Fields: `workflow_id` (uuid), `event_type` (start/step/end), `payload` (object), `timestamp` (iso8601).
4.  `chapters/brain/topic-orchestration/src/index.ts`
    *   **Prompt**: Entrypoint. Starts HTTP server. Loads config. Logs startup.
5.  `chapters/brain/topic-orchestration/test/smoke.test.ts`
    *   **Prompt**: Verifies module imports and basic unit logic.

**Verification**:
*   `pnpm install` works.
*   `pnpm build` passes (tsc).
*   `pnpm test` passes.
*   Pipe schema validates against meta-schema.

#### UMP-0111: State Machine Logic
**Title**: Implement WorkItem State Machine.
**Scope**: `chapters/brain/topic-orchestration/src/**`

**Files to Create**:

1.  `chapters/brain/topic-orchestration/src/state_machine.ts`
    *   **Prompt**: Define `WorkItemState` enum (New, Triaged, Processing, Actionable, Done). Implement `transition(current, event) -> next`. Enforce valid transitions only.
2.  `chapters/brain/topic-orchestration/test/state_machine.test.ts`
    *   **Prompt**: Unit tests for all valid and invalid transitions.

**Verification**:
*   100% coverage of state transitions.

#### UMP-0112: Processor Logic Migration
**Title**: Migrate Processor Logic from Spine.
**Scope**: `chapters/brain/topic-orchestration/src/**`

**Files to Create**:

1.  `chapters/brain/topic-orchestration/src/processor.ts`
    *   **Prompt**: Port logic from `spine/chapters/intelligence/processor.py`. Adapt Python to TypeScript.
    *   **Logic**: Receive `StreamEvent` -> Check Idempotency -> Run Triage -> Update State.
    *   **Note**: "Check Idempotency" and "Run Triage" must be **In-Process Interface Calls** (Interfaces defined here, implemented by adapters later) or **Pipe Events**. *Decision: Use Pipe Events for strict decoupling.*

**Verification**:
*   Unit tests mocking the Pipe inputs/outputs.

---

## 3. Inventory & Gap Analysis

**Current Inventory State**:
We have a python monolith in `spine/`. We are planning a move to `chapters/` (TS/Polyglot compatible structure).

**Identified Gaps**:
1.  **Language Stack**: User requested TS/Node for `chapters` in previous prompt defaults, but `spine` is Python.
    *   *Correction*: We should keep `spine` (Python) as the Core/DB layer and build new `chapters` as Python modules *first* to minimize rewrite risk, OR explicitly decide to rewrite in TS.
    *   *Decision*: **Stick to Python for Backend (Brain/Spine)** to utilize existing code. The "Canonical UMP" defaults said TS, but our code is Python.
    *   *Correction*: **UMP-0110** above should generate `pyproject.toml` not `package.json`.

**Revised UMP-0110 (Python Version)**:
1.  `chapters/brain/topic-orchestration/pyproject.toml`
2.  `chapters/brain/topic-orchestration/src/__init__.py`
3.  `chapters/brain/topic-orchestration/tests/test_smoke.py`

---

## END OF PHASE 3 OUTPUT — Type: PROCEED PHASE 4
