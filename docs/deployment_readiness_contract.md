
# Deployment Readiness Contract (DRC) - v1.1 (Strict Visual)

**Objective**: Define the absolute "GO / NO-GO" criteria for deploying `assistants-co-system`. This contract overrides all other decisions.

## 1. The "Must-Have" Feature Set (Vertical Slice v0)
The system is allowed to ship ONLY when the following path is operational end-to-end:
1.  **User Signup/Login**: OAuth (Gmail/Outlook) works.
2.  **Ingestion**: System reads *one* email from the provider.
3.  **Drafting**: System generates *one* draft reply (AI/Template).
4.  **Review**: User approves the draft.
5.  **Send**: System sends the email via the provider API.
*(No dashboards, no billing, no complex policies required for v0).*

## 2. The Strict Protocol (Development Gates)
Every UMP, Phase, Topic, and Chapter MUST pass this sequence before Sealing:

1.  **Inventory Check**:
    *   Check `inventory.md` for existing files.
    *   Prevent duplication.
2.  **Code Implementation**:
    *   Write/Modify code in the correct `feature/` branch.
3.  **Existing Tests**:
    *   Run `pytest` (Backend) or `npm test` (Frontend).
4.  **Visual Verification (Browser)**:
    *   **Action**: Agent opens the Feature in a Browser (Swagger UI for Backend, React App for Frontend).
    *   **Capture**: Agent takes a **Screenshot** of the success state.
5.  **AI Verification**:
    *   **Action**: Agent *reads* the Screenshot.
    *   **Logic**: Does the image match the "Pass" criteria?
6.  **Inventory Update**:
    *   Update `inventory.md` with: File Path, Description, Context, and Current Branch.
7.  **Seal**:
    *   Only *then* is the feature marked "Sealed".
    *   Push to GitHub -> CI/CD -> AWS.

## 3. Quantitative Gates (Automated)
*   **Test Pass Rate**: 100% (Blocker).
*   **Tenant Isolation Check**: `test_tenant_isolation.py` MUST pass.
*   **Vulnerability Scan**: No High/Critical CVEs in deps.
*   **Build Artifact**: Docker image builds successfully.

## 4. Operational Gates (Manual/HITL)
*   **Visual Confirmation**: Screenshot of the "Review" UI state.
*   **Inventory Seal**: All UMPs in `inventory.md` marked `Sealed`.
*   **Authority Check**: Deployment triggered ONLY by `USER` or `ADMIN` role.

**Signed**,
*Canonical UMP Architect*
