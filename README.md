# Email Systems (Antigravity)

**Project Phase**: Phase 1 Complete (Infrastructure Sealed)

## Overview
This project implements a secure, scalable email system functionality for Assistants Company, starting with AWS Infrastructure.

## Architecture
- **Phase 0**: Foundation (Identity, Audit, Verification).
- **Phase 1**: Infrastructure (AWS Organization, VPC, EKS, RDS, Redis, S3, CI/CD, Observability).
- **Phase 2**: App Core (Backend API).

## Functional Architecture (The "Brain")
This system operates on a **Zero-Storage** principle to maximize privacy and security.

1.  **The Pipe (Streamer)**: Connects to Gmail and streams emails into memory.
2.  **The Logic (Triage)**: Analyzes Metadata (Subject, Sender, Date) *without* reading the body to determine Urgency and Category.
3.  **The Memory (Processor)**: Saves a "WorkItem" (pointer) to the database, but *discards* the email body.
4.  **The Interface (Live Proxy)**: When you click an email in the UI, the frontend fetches the body *live* from Gmail, keeping the backend database clean.
5.  **The Hands (Action)**:
    -   **Vault**: Securely stores encryption keys (PAN, DOB, etc.).
    -   **Unlocker**: Decrypts attachments on-demand using Vault keys.


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
This project adheres to strict governance protocols:
- **Diamond Brick Protocol**: Branch -> Code -> Test -> Visual -> Seal.
- **Inventory**: All files tracked in `inventory.md`.
- **Verification**: Visual proofs required for all chapters.

---
*Built with Governance by NerdyFox Co.*
