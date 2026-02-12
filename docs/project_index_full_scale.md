
# Phase 4 — Canonical UMP: Full Scale Project Index & Gaps

**Objective**: Produce the **Full-Scale Project Index** (Authoritative Map) for `assistants-co-system` (formerly fyxer-engine), incorporating deep gaps identified from the `Fyxer` reference material.

> **CRITICAL PIVOT**: The reference material mandates a "Unified Canonical Implementation Spine" starting with **Phase 0 (Foundation)** and **Chapter 0 (Execution Authority)**. I have adjusted the index to reflect this absolute requirement.

---

## 1. Phase 0: Foundation (Immutable Spine)

### CH-00: Foundation (Shared Infrastructure)
**Path**: `foundation/`
- [ ] **TP-01: Authority** (Execution Control)
    - [ ] PH-01: Authority Contract (User > HITL > AI)
    - [ ] PH-02: Stop Engine (Fail Closed)
- [ ] **TP-02: Identity** (Tenant Core)
    - [ ] PH-01: Tenant Model (Hard Isolation)
    - [ ] PH-02: Role Matrix (RBAC)
- [ ] **TP-03: Audit** (Ledger)
    - [ ] PH-01: Immutable Audit Log (Hash Chain)
- [ ] **TP-04: Inventory** (Artifact Tracking)
    - [ ] PH-01: Inventory Ledger

---

## 2. Project Index (Functional Chapters)

### 🧠 CH-01: Brain (The Strategist)
**Path**: `chapters/brain/`
- [ ] **TP-01: Orchestration** (Workflow Engine)
    - [ ] PH-01: State Machine (Migrate from Spine)
- [ ] **TP-02: Triage** (Smart Categorization) **[GAP FILL]**
    - [ ] PH-01: Classifier Model (To Respond, FYI, etc.)
    - [ ] PH-02: Heuristic Rules Engine
- [ ] **TP-03: Tone Learning** (Personalization) **[GAP FILL]**
    - [ ] PH-01: User Embeddings (Compact Profile)
    - [ ] PH-02: Tone Templates (30 Standard Styles)
    - [ ] PH-03: Context Classification (Style Selector)

### 🤚 CH-02: Hands (The Actuator)
**Path**: `chapters/hands/`
- [ ] **TP-01: Composer** (Drafting)
    - [ ] PH-01: LLM Draft Generation (RAG-based)
    - [ ] PH-02: Template Engine
- [ ] **TP-02: Valve** (Safety)
    - [ ] PH-01: Approval Gate (User Review Mandatory)
    - [ ] PH-02: Send Execution

### 👀 CH-03: Eyes (The Sensor)
**Path**: `chapters/eyes/`
- [ ] **TP-01: Ingestion** (Integrations)
    - [ ] PH-01: Gmail API (Migrate)
    - [ ] PH-02: Outlook Graph API **[GAP FILL]**
    - [ ] PH-03: Calendar API **[GAP FILL]**
- [ ] **TP-02: Meetings** (Notes) **[GAP FILL]**
    - [ ] PH-01: Transcript Ingestion
    - [ ] PH-02: Summarization

### 🦵 CH-04: Legs (The Runner)
**Path**: `chapters/legs/`
- [ ] **TP-01: Scheduler** (Cron)
- [ ] **TP-02: Workers** (Async Jobs)

### ❤️ CH-05: Heart (The Stabilizer)
**Path**: `chapters/heart/`
- [ ] **TP-01: Reliability** (Idempotency)
- [ ] **TP-02: Health** (Observability)

### 🩸 CH-06: Kidneys (The Filter)
**Path**: `chapters/kidneys/`
- [ ] **TP-01: HITL** (Human Loop)
    - [ ] PH-01: Escalation Queue
    - [ ] PH-02: Evidence Contract
- [ ] **TP-02: Compliance** (Privacy)
    - [ ] PH-01: Redaction
    - [ ] PH-02: Data Expiry

---

## 3. Gap Analysis Findings (from Fyxer Reference)

### A. Missing Functional Core
1.  **Outlook Integration**: Existing system is Gmail-only. Reference mandates Outlook Graph API.
2.  **Tone Learning**: Reference specifies "User Embeddings + Tone Templates" to scale to 1000 users. Current plan was generic LLM.
3.  **Smart Categorization**: Reference lists specific categories (To Respond, FYI, Awaiting Reply) that must be auto-labeled.
4.  **Meeting Notes**: Reference includes Calendar sync and Meeting summarization as core features.

### B. Missing Operational Spine (Crucial)
1.  **Execution Authority**: Reference mandates a specific "Authority Contract" UMP to prevent AI overreach.
2.  **Immutable Audit**: Reference requires a cryptographic hash chain for all actions.
3.  **Tenant Isolation**: Reference requires Hard SQL isolation for multi-tenancy.

### C. Infrastructure Gaps
1.  **Kubernetes (EKS)**: Reference mandates EKS for deployment (we assumed Docker/K8s but need specific manifests).
2.  **AWS Identity**: Reference specifies IAM roles (platform-admin, eks-cluster-role).

---

## 4. Execution Plan Adjustments

1.  **Phase 0 (Foundation)** must be executed **FIRST**. We cannot build "Brain" (CH-01) without the "Authority" and "Tenant" models from CH-00.
2.  **Rename Project**: Reference suggests `Assistant Co` / `Assistants Co`. I will use `assistants-co-system` as the canonical keys.

## END OF PHASE 4 OUTPUT — Type: PROCEED IMPLEMENTATION
