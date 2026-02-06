# Fyxer SaaS Implementation Plan (Canonical Execution Graph)

> [!IMPORTANT]
> **GOVERNANCE ENFORCEMENT**: This document is the **Law**. It defines the **Canonical Repository Tree** down to the atomic **Ultra Micro Phase (UMP)** level.
> **STRICT ADHERENCE**: No Agent may create a file that is not explicitly defined in this graph.
> **MODULE RULE**: Every Chapter is a self-contained module. No cross-chapter imports. Shared foundation only.
> **VISUAL VERIFICATION**: Every UMP *must* be visibly tested (Screenshot/Terminal Read) before sealing.

---

## 🚦 The UMP Execution Template (THE CONTRACT)

**Every Single UMP** listed below must be executed using this exact workflow. **Do not deviate.**

1.  **Inventory Check**:
    -   Command: `grep -r "Function Name" foundation/docs/INVENTORY_LIST.md`
    -   Rule: If functionality exists, **STOP**. Do not duplicate.
2.  **Branch Creation**:
    -   Command: `git checkout -b feat/<UMP_ID>` (e.g., `feat/CH00-T01-UMP001`)
3.  **File Creation** (The "Brick"):
    -   You must create **ALL** of the following files for every UMP:
        *   `CONTEXT.md`: Context, Purpose, Connectivity (Pipes).
        *   `PROMPT.md`: The exact prompt used to generate the code.
        *   `SPEC.json`: The JSON explaining specifics.
        *   `[CODE_FILE]`: The actual logic/schema file (inside `allowed_roots`).
        *   `TEST_VISUAL.py`: A script that produces visible output (CLI or Browser).
4.  **Visual Verification**:
    -   Run `python TEST_VISUAL.py` (or start server).
    -   **Capture Evidence**: Use `read_terminal` or `browser_screenshot` to see the result.
    -   **Agent Confirmation**: "I have visually confirmed the test passed."
5.  **Sealing**:
    -   Run `sha256sum * > SEAL.md`.
    -   Append entry to `foundation/docs/INVENTORY_LIST.md`.
    -   Commit & Push: `git add . && git commit -m "Seal <UMP_ID>" && git push origin feat/<UMP_ID>`

---

## 🌳 The Canonical Execution Graph

### 🧱 Chapter 00: Governance Kernel
*Function: Define the rules of physics. No runtime logic.*

#### 📘 Topic T01: Canonical Definitions
*Blueprint: The JSON Schemas that define the system itself.*

##### 🔹 Phase PH01: Core Objects

###### 🧱 UMP-001: Define Chapter, Topic, UMP & Pipe Schemas
*   **Branch**: `feat/CH00-T01-UMP001`
*   **Inventory Check**: Search for `Core Objects Schema`.
*   **Files to Create**:
    1.  `chapters/CH00/topics/T01/phases/PH01/umps/UMP001/CONTEXT.md`
        *   **Context**: The system needs self-awareness of its own structure.
        *   **Connectivity**: Pipes `PIPE_GOV_DEF` to all Chapters.
    2.  `chapters/CH00/topics/T01/phases/PH01/umps/UMP001/PROMPT.md`
        *   **Content**: "Generate JSON schemas for Chapter, Topic, UMP, and Pipe."
    3.  `chapters/CH00/topics/T01/phases/PH01/umps/UMP001/SPEC.json`
        *   **Specifics**: Regex patterns for IDs, Enums for Pipe Rules.
    4.  `foundation/contracts/core_objects.schema.json` (The Code)
        *   **Purpose**: Validates the repo structure.
    5.  `foundation/contracts/pipe.schema.json` (The Code)
        *   **Purpose**: Validates data flow.
    6.  `chapters/CH00/topics/T01/phases/PH01/umps/UMP001/TEST_VISUAL.py`
        *   **Purpose**: Validates sample JSON against the schemas and prints "SUCCESS" in green.
*   **Verification**: Run `TEST_VISUAL.py` -> Capture Terminal -> Confirm "SUCCESS".

###### 🧱 UMP-002: Define Module Packaging Rule
*   **Branch**: `feat/CH00-T01-UMP002`
*   **Inventory Check**: Search for `Module Packaging Rule`.
*   **Files to Create**:
    1.  `chapters/CH00/topics/T01/phases/PH01/umps/UMP002/CONTEXT.md`
    2.  `chapters/CH00/topics/T01/phases/PH01/umps/UMP002/PROMPT.md`
    3.  `chapters/CH00/topics/T01/phases/PH01/umps/UMP002/SPEC.json`
    4.  `foundation/contracts/module_rule.schema.json` (The Code)
        *   **Purpose**: Defines `allowed_roots` for every Chapter.
    5.  `chapters/CH00/topics/T01/phases/PH01/umps/UMP002/TEST_VISUAL.py`
        *   **Purpose**: Checks if a mock file path violates the rule and prints the result.
*   **Verification**: Run `TEST_VISUAL.py` -> Capture Terminal -> Confirm Enforcement.

#### 📘 Topic T02: Sealing & Evidence
##### 🔹 Phase PH01: Proof Templates

###### 🧱 UMP-001: Define Proof & Seal Templates
*   **Branch**: `feat/CH00-T02-UMP001`
*   **Inventory Check**: Search for `Proof Template`.
*   **Files to Create**:
    1.  `chapters/CH00/topics/T02/phases/PH01/umps/UMP001/CONTEXT.md`
    2.  `chapters/CH00/topics/T02/phases/PH01/umps/UMP001/PROMPT.md`
    3.  `chapters/CH00/topics/T02/phases/PH01/umps/UMP001/SPEC.json`
    4.  `foundation/docs/templates/PROOF_TEMPLATE.md` (The Code)
    5.  `foundation/docs/templates/SEAL_TEMPLATE.md` (The Code)
    6.  `chapters/CH00/topics/T02/phases/PH01/umps/UMP001/TEST_VISUAL.py`
        *   **Purpose**: Renders the templates to console for inspection.
*   **Verification**: Run `TEST_VISUAL.py` -> Capture Terminal -> Confirm Layout.

---

### bone 🦴 Chapter 01: Foundation Spine
*Function: The Shared Runtime Substrate.*

#### 📘 Topic T01: Runtime Spine
##### 🔹 Phase PH01: System Primitives

###### 🧱 UMP-001: Config Loader (Fail-Closed)
*   **Branch**: `feat/CH01-T01-UMP001`
*   **Inventory Check**: Search for `Config Loader`.
*   **Files to Create**:
    1.  `chapters/CH01/topics/T01/phases/PH01/umps/UMP001/CONTEXT.md`
    2.  `chapters/CH01/topics/T01/phases/PH01/umps/UMP001/PROMPT.md`
    3.  `chapters/CH01/topics/T01/phases/PH01/umps/UMP001/SPEC.json`
    4.  `foundation/runtime/config.py` (The Code)
        *   **Purpose**: Loads `APP_ENV`. Hard crash if missing.
    5.  `chapters/CH01/topics/T01/phases/PH01/umps/UMP001/TEST_VISUAL.py`
        *   **Purpose**: Runs `config.py` without env var (Expect Crash), then with env var (Expect Success).
*   **Verification**: Run `TEST_VISUAL.py` -> Capture Terminal -> Confirm Fail-Closed behavior.

###### 🧱 UMP-002: Request Context (Tenant Binding)
*   **Branch**: `feat/CH01-T01-UMP002`
*   **Inventory Check**: Search for `Request Context`.
*   **Files to Create**:
    1.  `chapters/CH01/topics/T01/phases/PH01/umps/UMP002/CONTEXT.md`
    2.  `chapters/CH01/topics/T01/phases/PH01/umps/UMP002/PROMPT.md`
    3.  `chapters/CH01/topics/T01/phases/PH01/umps/UMP002/SPEC.json`
    4.  `foundation/runtime/context.py` (The Code)
        *   **Purpose**: ContextVar manager for Tenant/Actor.
    5.  `chapters/CH01/topics/T01/phases/PH01/umps/UMP002/TEST_VISUAL.py`
        *   **Purpose**: Simulates a request and prints context state.
*   **Verification**: Run `TEST_VISUAL.py` -> Capture Terminal -> Confirm Data Binding.

---

### 🏢 Chapter 02: Tenancy, Auth & Billing
*Function: Who moves the pipes.*

#### 📘 Topic T01: Tenancy Core
##### 🔹 Phase PH01: Tenant Model

###### 🧱 UMP-001: Tenant Model & Policy
*   **Branch**: `feat/CH02-T01-UMP001`
*   **Files**:
    *   `.../CONTEXT.md`, `.../PROMPT.md`, `.../SPEC.json`
    *   `chapters/CH02/topics/T01/contracts/tenant.schema.json` (The Code)
    *   `.../TEST_VISUAL.py`
*   **Verification**: Visual confirmation of Schema validation.

###### 🧱 UMP-002: Tenant Lifecycle Logic
*   **Branch**: `feat/CH02-T01-UMP002`
*   **Files**:
    *   `.../CONTEXT.md`, `.../PROMPT.md`, `.../SPEC.json`
    *   `chapters/CH02/topics/T01/logic/lifecycle.py` (The Code)
    *   `.../TEST_VISUAL.py` (Simulates Active vs Suspended tenant rights).
*   **Verification**: Visual confirmation that Suspended tenant is blocked.

---

### ⚙️ Chapter 04: Work Engine
*Function: The Token of Execution.*

#### 📘 Topic T01: Work Item
##### 🔹 Phase PH01: The Object

###### 🧱 UMP-001: WorkItem Schema
*   **Branch**: `feat/CH04-T01-UMP001`
*   **Files**:
    *   `.../CONTEXT.md`, `.../PROMPT.md`, `.../SPEC.json`
    *   `chapters/CH04/topics/T01/contracts/work_item.schema.json` (The Code)
    *   `.../TEST_VISUAL.py`
*   **Verification**: Visual confirmation of WorkItem structure.

##### 🔹 Phase PH02: State Machine

###### 🧱 UMP-001: State Transitions
*   **Branch**: `feat/CH04-T01-UMP002`
*   **Files**:
    *   `.../CONTEXT.md`, `.../PROMPT.md`, `.../SPEC.json`
    *   `chapters/CH04/topics/T01/logic/transitions.py` (The Code)
    *   `.../TEST_VISUAL.py` (Attempts illegal transitions).
*   **Verification**: Visual confirmation that DONE -> NOW is rejected.

---

### 🛡️ Chapter 10: Ops & Security
*Function: Production Safety.*

#### 📘 Topic T01: Secrets
##### 🔹 Phase PH01: Management

###### 🧱 UMP-001: Fail-Closed Secret Loader
*   **Branch**: `feat/CH10-T01-UMP001`
*   **Files**:
    *   `.../CONTEXT.md`, `.../PROMPT.md`, `.../SPEC.json`
    *   `foundation/runtime/secrets.py` (The Code)
    *   `.../TEST_VISUAL.py` (Attempts to load missing secret).
*   **Verification**: Visual confirmation of Hard Crash on missing secret.

---

## 📝 Inventory Integration & Sealing Rule

For **EVERY UMP** above:
1.  **Before Creation**: `grep` check against `foundation/docs/INVENTORY_LIST.md`.
2.  **After Verification**:
    -   Calculate SHA256 of all files.
    -   Write `SEAL.md`.
    -   Add row to `INVENTORY_LIST.md`: `| UMP-ID | Description | Sealed? YES |`
    -   `git push` to the `feat/` branch.
