# Fyxer: The Governed SaaS Operating System

> [!IMPORTANT]
> **GOVERNANCE ENFORCEMENT**: This repository follows a strict "Governance First" approach. 
> All code must adhere to the **Canonical Repository Tree** defined in the [Implementation Plan](implementation_plan.md).
>
> **FAIL-CLOSED**: The system is designed to fail-closed on any uncertainty or violation of guards.

## 📁 Repository Structure

The repository is organized into the following canonical roots:

*   **`foundation/`**: The **ONLY** allowed shared dependency surface. Contains Contracts, Runtime Primitives, and Guards.
*   **`chapters/`**: Self-contained, deployable modules (12 Chapters). No cross-chapter imports allowed.
*   **`spine/`**: Python package roots ensuring clean import paths.
*   **`apps/`**: Frontend applications (Next.js/React).
*   **`ops/`**: CI/CD pipelines, security scans, and operational scripts.

## 🚦 Execution Rules

1.  **Inventory First**: Before creating any file, check `foundation/docs/INVENTORY_LIST.md` to prevent duplication.
2.  **Ultra Micro Phases (UMPs)**: Development proceeds in atomic units (UMPs). 
    *   Each UMP is its own `feat/` branch.
    *   Each UMP produces 5 mandatory files: `CONTEXT`, `PROMPT`, `SPEC`, `CODE`, `TEST_VISUAL`.
3.  **Visual Verification**: No UMP is sealed until visually verified (Screenshot or Terminal Output).
4.  **Sealing**: Once verified, UMPs are sealed (hashed) and cannot be edited.

## 🛠️ Setup & Usage

### Prerequisites
*   Python 3.10+
*   Node.js 18+
*   Docker (for local services)

### Governance
Refer to `chapters/CH00_GOVERNANCE` for the core definitions and schemas that rule this system.

---
*Built with Governance by NerdyFox Co.*
