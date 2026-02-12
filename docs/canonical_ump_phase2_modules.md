
# Phase 2 — Canonical UMP: Module Instantiation (CH-01 to CH-07)

**Objective**: Define the exhaustive, authoritative list of **Chapters**, **Topics**, **Phases**, and **UMPs** to migrate the existing `spine` monolith into the Canonical `chapters/` organ architecture.

---

## CH-01: Brain (The Strategist)
**Purpose**: Deterministic orchestration, workflow state machine, policy coordination, and triage logic.
**Module Folder**: `chapters/brain/`
**Target**: `spine/chapters/mind/` + `spine/chapters/intelligence/processor.py` (Logic part).

### TP-01: topic-triage (The Classifier)
**Blueprint**: Intelligent classification of incoming data.
- **PH-01: Contracts & Skeleton**
    - **UMP-0101**: Create `topic-triage` skeleton & `pipe.triage.request.v1` schema.
    - **UMP-0102**: Migrate `spine/chapters/intelligence/triage.py` to `src/logic.py`.
    - **UMP-0103**: Implement Consumer (`lungs` -> `brain`).
- **PH-02: Decision Logic**
    - **UMP-0104**: Migrate Urgency/Date/Spam logic.
    - **UMP-0105**: Connect to `pipe.triage.result.v1` (Producer).
    - **UMP-0106**: Verify 10-Tests (Urgent, VIP, Spam, etc.).

### TP-02: topic-orchestration (The Conductor)
**Blueprint**: Workflow Engine & State Machine.
- **PH-01: Contracts & Skeleton**
    - **UMP-0110**: Create `topic-orchestration` skeleton & `pipe.workflow.event.v1`.
    - **UMP-0111**: Define `WorkItemState` transitions (State Machine).
- **PH-02: Processor Logic (Migration)**
    - **UMP-0112**: Migrate `spine/chapters/intelligence/processor.py` (State Logic only).
    - **UMP-0113**: Implement Idempotency Check (calls `Heart`).
    - **UMP-0114**: Implement Persistence (calls `Spine` Core DB).

### TP-03: topic-policy (The Judge)
**Blueprint**: Deployment Readiness & Execution Mandates.
- **PH-01: Primitives**
    - **UMP-0120**: Create `topic-policy` skeleton.
    - **UMP-0121**: Implement `DeploymentReadiness` checks (JSON Logic).
    - **UMP-0122**: Implement `ExecutionMandate` checks (Shutoff/Throttle).

---

## CH-02: Hands (The Actuator)
**Purpose**: Write actions, mutations, external side-effects (Sending emails, calling webhooks).
**Module Folder**: `chapters/hands/`
**Target**: `spine/chapters/action/`

### TP-01: topic-composer (The Writer)
- **PH-01: Migration**
    - **UMP-0201**: Create skeleton & `pipe.draft.request.v1`.
    - **UMP-0202**: Migrate `spine/chapters/action/composer.py`.
    - **UMP-0203**: Connect to Gmail API (via Foundation helper).

### TP-02: topic-valve (The Safety)
- **PH-01: Migration**
    - **UMP-0210**: Create skeleton & `pipe.send.request.v1`.
    - **UMP-0211**: Migrate `spine/chapters/action/valve.py`.
    - **UMP-0212**: Implement "Safe Mode" check (calls `Brain` Policy).

### TP-03: topic-vault (The Secrets)
- **PH-01: Migration**
    - **UMP-0220**: Create skeleton.
    - **UMP-0221**: Migrate `spine/chapters/action/vault.py` & `unlocker.py`.
    - **UMP-0222**: Expose `decrypt` function via Inter-Process pipe only.

---

## CH-03: Eyes (The Sensor)
**Purpose**: Ingestion, Live Readers, Sensors.
**Module Folder**: `chapters/eyes/`
**Target**: `spine/chapters/intelligence/proxy.py`

### TP-01: topic-proxy (The Live Reader)
- **PH-01: Migration**
    - **UMP-0301**: Create skeleton & `pipe.fetch.body.v1`.
    - **UMP-0302**: Migrate `spine/chapters/intelligence/proxy.py`.
    - **UMP-0303**: Validation: Ensure HTML Sanitization (calls `Kidneys` or internal lib).

### TP-02: topic-ingestion (The Batch)
- **PH-01: History**
    - **UMP-0310**: Create `topic-ingestion` skeleton.
    - **UMP-0311**: Implement "Warm Start" (Fetch last N emails). (Gap Fix)

---

## CH-04: Legs (The Runner)
**Purpose**: Workers, Cron, Async Schedulers.
**Module Folder**: `chapters/legs/`
**Target**: `spine/chapters/workers` (To be created).

### TP-01: topic-scheduler
- **PH-01: Cron**
    - **UMP-0401**: Create skeleton.
    - **UMP-0402**: Implement Distributed Lock (Redis).
    - **UMP-0403**: Schedule "Poll Gmail" job.

### TP-02: topic-worker
- **PH-01: Async Runners**
    - **UMP-0410**: Create generic Job Runner.
    - **UMP-0411**: Bind to Redis Streams types.

---

## CH-05: Heart (The Stabilizer)
**Purpose**: Reliability, Idempotency, Retries, DLQ.
**Module Folder**: `chapters/heart/`

### TP-01: topic-idempotency
- **PH-01: Deduplication**
    - **UMP-0501**: Create skeleton.
    - **UMP-0502**: Implement `check_processed(id, tenant_id)`.
    - **UMP-0503**: Implement Redis-based short-term memory + DB long-term check.

### TP-02: topic-health
- **PH-01: DLQ**
    - **UMP-0510**: Create Dead Letter Queue handler.
    - **UMP-0511**: Implement Retry Policy (Exponential Backoff).

---

## CH-06: Lungs (The Stream)
**Purpose**: Streaming, Buffering, Backpressure.
**Module Folder**: `chapters/lungs/`
**Target**: `spine/chapters/intelligence/streamer.py`.

### TP-01: topic-streamer
- **PH-01: Migration**
    - **UMP-0601**: Create skeleton & `pipe.stream.event.v1`.
    - **UMP-0602**: Migrate `spine/chapters/intelligence/streamer.py`.
    - **UMP-0603**: Implement Generator -> Redis Publisher pattern.

---

## CH-07: Kidneys (The Filter)
**Purpose**: Validation, Compliance, Redaction, HITL.
**Module Folder**: `chapters/kidneys/`
**Target**: `spine/chapters/hitl`, `spine/chapters/admin`.

### TP-01: topic-hitl (The Human Queue)
- **PH-01: Migration**
    - **UMP-0701**: Create skeleton & `pipe.hitl.request.v1`.
    - **UMP-0702**: Migrate `spine/chapters/hitl`.
    - **UMP-0703**: Verify Escalation Logic.

### TP-02: topic-compliance (The Auditor)
- **PH-01: Redaction**
    - **UMP-0710**: Create PII Redactor service.
    - **UMP-0711**: Implement "Right to be Forgotten" (Data Flush).

### TP-03: topic-admin (The Overseer)
- **PH-01: Migration**
    - **UMP-0720**: Create skeleton.
    - **UMP-0721**: Migrate `spine/chapters/admin` (Tenants, Billing, Safety).

---

# Execution Mandate (Phase 2)
The existing `spine` code is "Monolithic Modular" (folders within a monolith).
**Transition Plan**:
1.  **Skeleton**: Create `chapters/` structure.
2.  **Contracts**: Define Pipes.
3.  **Lift & Shift**: Move logic from `spine/chapters/` to `chapters/<organ>/topic/src/`.
4.  **Wire**: Replace direct imports with Pipe calls.
5.  **Seal**: Lock the new UMPs.
6.  **Decommission**: Remove `spine/chapters/` (Legacy).

## END OF PHASE 2 OUTPUT — Type: PROCEED PHASE 3
