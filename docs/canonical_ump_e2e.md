
# Phase 1 — Canonical Meta-Prompt (Ultra Micro Plan – E2E)

## 1. Objective
Design and output an **Ultra Micro Plan – E2E** for the "Email Systems" (Fyxer) platform using a **strict, deterministic, agent-oriented structure**. The goal is to enforce **module packaging**, **canonical repo tree**, **phase-wise sequencing**, and **guardrails** to transition from a "Project" to a "Product".

## 2. System Role
**Canonical UMP Architect & Repo Enforcer**.

## 3. Inputs

### ASSUMED_DEFAULTS
- **PROJECT_NAME**: `fyxer-engine`
- **PROJECT_DOMAIN**: **Autonomous Email Intelligence & Action Platform**
- **PRIMARY_LANG_STACK**: **Python 3.12+ (Backend/Spine), TypeScript/React (Frontend/Face)**
- **RUNTIME_TARGET**: **Docker + Kubernetes (EKS)**
- **DEPLOYMENT_MODEL**: **Mono-repo (Canonical)**
- **DATA_CLASSIFICATION**: **Internal/Confidential (Strict PII/User Data Rules)**
- **INTERFACE_SURFACES**: **API (FastAPI), UI (React), Events (Redis/Streams)**
- **ORGANS_REQUIRED**: **Brain (Logic), Hands (Action), Eyes (Ingestion), Legs (Workers), Heart (Reliability), Lungs (Streaming), Kidneys (Validation/Compliance)**.
- **SHARED_FOUNDATION_ALLOWED**: **True** (Strictly limited to `foundation/`).
- **TEST_LEVELS_REQUIRED**: **Unit, Contract, Integration, E2E**.
- **CI_SYSTEM**: **GitHub Actions**.

---

## 4. Architecture Expectations

### A. Zero-Storage Architecture (Confirmed)
> **Constraint**: We do **NOT** store tenant raw data (email bodies, attachments) persistently in our primary database.
- **Streaming Only**: The `Lungs` and `Eyes` modules stream data from the Source of Truth (Gmail/Outlook) on demand.
- **Metadata Persistence**: We ONLY persist:
    - **IDs**: `provider_message_id`, `thread_id` (Mapped to Tenant).
    - **Heuristics**: Triage scores, tags, urgency flags (`Brain` output).
    - **State**: `WorkItem` status, `Workflow` transitions.
    - ** Vectors**: (Optional) Ephemeral embeddings for active context, purged per policy.
- **Burden of Truth**: The user's external provider (Gmail) is the Source of Truth. We are the **Intelligence Overlay**.

### B. Spine-and-Organs Model
- **Spine** (`spine/`): The "Nervous System".
    - **Pipe Registry**: Defines ALL valid data pathways.
    - **Contract Enforcement**: run-time schema validation.
    - **Identity & Auth**: `User`, `Tenant`, `Scope` global definitions.
- **Organs** (`chapters/`): Enforced Interface Domains.
    - **Brain** (`spine/chapters/mind` + `intelligence`): Workflow Engine, Policy, Triage Logic. 
    - **Hands** (`spine/chapters/action`): Actuators, Draft Composer, Valve (Sender).
    - **Eyes** (`spine/chapters/intelligence/proxy`): Ingestion, Live Readers, Sensors.
    - **Legs** (`spine/chapters/workers`): Job Runners, Cron, Async Schedulers.
    - **Heart** (`spine/chapters/health`): Reliability, Idempotency, Retries, DLQ.
    - **Lungs** (`spine/chapters/intelligence/streamer`): Streaming, Buffering, Backpressure.
    - **Kidneys** (`spine/chapters/hitl` + `admin`): Validation, Compliance, Redaction, HITL Queues.

### C. Pipes
- **Rule**: No module calls another module's internal code.
- **Mechanism**: 
    - **Inter-Process**: Redis Streams / Event Bus (Async).
    - **In-Process**: Strict Interface Contracts (Sync).
- All exchange must be defined in `foundation/contracts/pipes/`.

---

## 5. Canonical Repository Tree

```
fyxer-engine/
  README.md
  pyproject.toml                       # Root dependencies
  alembic.ini                          # DB Migrations (Global)
  
  docs/                                # Governance & Plans
    architecture/
    contracts/
    runbooks/
    ump/
  
  foundation/                          # SHARED SURFACE (No Business Logic)
    contracts/                         # JSON Schemas / Pydantic Models
    lib/                               # Logging, Security, Validation Utils
    testing/                           # Test Runners, Fixtures
  
  spine/                               # BACKEND MONOLITH (Modular)
    main.py                            # Entrypoint
    core/                              # Config, Middleware
    db/                                # Base Models, Session Manager
    
    chapters/                          # THE ORGANS
      brain/                           # Logic & Decisions
      hands/                           # Action & Output
      eyes/                            # Ingestion & Sensing
      legs/                            # Workers & Scheduling
      heart/                           # Reliability & Health
      lungs/                           # Streaming & Buffering
      kidneys/                         # Compliance & Admin
  
  face/                                # FRONTEND (The Face)
    src/
      chapters/                        # UI mapped to Organs
      components/                      # Shadcn UI
      features/                        # Auth, Global State
  
  infrastructure/                      # IaC
    aws/
    k8s/
    local/
    
  scripts/                             # Operational Scripts
    bootstrap/
    maintenance/
    test/
```

---

## 6. Module Packaging & Enforcement Rules

### A. Dependency Rules
1. **Foundation First**: `foundation` depends on NOTHING.
2. **Spine Core**: Depends on `foundation`.
3. **Chapters**: Depend on `spine.core` + `foundation`.
    - **Forbidden**: `chapters/brain` imports `chapters/hands`.
    - **Allowed**: `chapters/brain` emits `Event` -> `Spine` -> `chapters/hands`.

### B. Sealing Rules (Immutability)
- **UMP Completion**: Requires `seal.json` in the UMP folder.
- **Content**:
    - List of modified files.
    - SHA256 hashes.
    - Test Execution Log.
- **Enforcement**: CI fails if a Sealed file is modified without a new UMP ID.

---

## 7. UMP Global Guardrails

1.  **Atomicity**: One UMP = One verifiable unit of value.
2.  **Contracts First**: Define the Pydantic Model / JSON Schema/ Interface BEFORE implementation.
3.  **Verification**: Every UMP must have a `verify.py` or specific `pytest` command.
4.  **No "TBD"**: Ambiguity is a failure state.
5.  **Rollback**: Database migrations must have `downgrade`.

---

## 8. Chapters (Function Modules)

### CH-01: Brain (The Strategist)
- **Topic**: Orchestration & Triage.
- **Phases**:
    - **PH-01**: Triage Logic (Implemented).
    - **PH-02**: Context Assembly (Implemented).
    - **PH-03**: Decision Engine (Active).

### CH-02: Hands (The Actuator)
- **Topic**: Drafting & Sending.
- **Phases**:
    - **PH-01**: Composer (Implemented).
    - **PH-02**: Valve/Safety (Implemented).
    - **PH-03**: Vault/Encryption (Implemented).

### CH-03: Eyes (The Sensor)
- **Topic**: Ingestion.
- **Phases**:
    - **PH-01**: Proxy/Live Read (Implemented).
    - **PH-02**: Graph API Integration (Gap - Planner).

### CH-04: Legs (The Runner)
- **Topic**: Async Execution.
- **Phases**:
    - **PH-01**: Background Workers (Gap - Planner).
    - **PH-02**: Scheduling (Gap - Planner).

### CH-05: Heart (The Stabilizer)
- **Topic**: Reliability.
- **Phases**:
    - **PH-01**: Idempotency (Implemented - Tenant Isolation).
    - **PH-02**: Dead Letter Queues (Gap - Planner).

### CH-06: Lungs (The Stream)
- **Topic**: Throughput.
- **Phases**:
    - **PH-01**: Streamer (Implemented).
    - **PH-02**: Backpressure (Gap - Planner).

### CH-07: Kidneys (The Filter)
- **Topic**: Compliance & Admin.
- **Phases**:
    - **PH-01**: Validation (Implemented).
    - **PH-02**: HITL/Escalation (Implemented).
    - **PH-03**: Admin Controls (Implemented).

---

## END OF PHASE 1 OUTPUT — Type: PROCEED PHASE 2
