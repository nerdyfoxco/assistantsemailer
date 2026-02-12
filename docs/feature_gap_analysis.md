
# Deep-Dive Feature Audit & Gap Analysis
**Scope**: Channels 0-11 (Current) vs. Fyxer Legacy Specs (Full Deep Dive including UI/UX Parts 2-6)
**Date**: 2026-02-11
**Status**: CRITICAL GAPS IDENTIFIED

## 🚨 1. Structural & Governance Gaps (The "Why It Didn't Ship" Root Cause)
The current system has perfect *internal* consistency but lacks the *execution permissions* to be a deployable SaaS.

| Missing Primitive | Description | Impact |
|-------------------|-------------|--------|
| **Deployment Readiness Contract (DRC)** | A machine-checkable JSON object defining exactly when "v0" is done. | **BLOCKER**: AI cannot know when to stop building. |
| **Execution Mandate** | An explicit authority window allowing the AI to "stub" non-critical features. | **BLOCKER**: System strives for infinite perfection instead of shipping. |
| **Vertical Slice Definition** | A formal definition of the *exact* loop: `User -> Inbox -> Draft -> Approve -> Send -> Close`. | **BLOCKER**: Horizontal building (layers) instead of vertical building (features). |
| **Bootstrap Guard Profile** | A temporary relaxation of strict security rules (e.g., allow "trust first") for v0. | **BLOCKER**: Production-grade security prevents valid bootstrap actions. |
| **Mandatory Structure** | The user strictly enforces `Chapter > Topic > Phase > UMP` hierarchy. | **RISK**: Current structure is mostly aligned but needs strict adherence. |

---

## 2. Functional Gaps (The "Missing Features")

### 📅 Calendar & Meetings (Major Gap)
- [ ] **Smart Scheduling**: Suggesting times, "Calendly-style" links.
- [ ] **Meeting Notes**: Joining calls, transcribing, summarizing.
- [ ] **Calendar Intel**: Reading events to inform email context (e.g., "I see you have a meeting with Bob").

### 📧 Email & Integration Depth
- [ ] **Outlook Integration**: Graph API support (currently Gmail only).
- [ ] **Historical Ingestion**: "Warm Start" analysis of last 300-500 sent emails to learn tone *before* Day 1.
- [ ] **Backlog Cleanup**: Automated "Zeroing" of old inbox (Archive/Unsubscribe bulk actions).
- [ ] **Knowledge Graph**: Persistent graph of People/Companies/Relationships (currently transient context only).
- [ ] **Data Gap Resolution**: Explicit "Where did this come from?" loop using Playwright/HITL.

### 🏢 Operations & Surfaces (The "7 Surfaces")
We have ~3 partially verified (Public, User, Admin). We are missing:
- [ ] **Support Surface**: Ticketing and user-state debugging.
- [ ] **Sales Surface**: Funnel tracking, lead scoring, demo playback.
- [ ] **Partner Portal**: API keys and webhooks.
- [ ] **Marketing Dashboard**: Affiliate tracking, ad funnels.

### 📈 Growth & Compliance
- [ ] **Growth Stack**: Google Tag Manager, GA4, Meta Pixel, LinkedIn Insight.
- [ ] **compliance**: GDPR Export, SOC-2 Evidence Generator.

---

## 3. Implemented & Verified Features (Our Solid Foundation)
These are **SEALED** and ready to support the missing pieces.

### 🏗️ Foundation & Infrastructure
- [x] **AWS Cloud Native**: EKS, RDS, Redis, IAM.
- [x] **Multi-Tenant**: Strict Row-Level Security.

### 🧠 Intelligence Engine
- [x] **Zero-Storage Triage**: Streaming classification, metadata only.
- [x] **Ephemeral Body Proxy**: Safe HTML fetching.
- [x] **Smart Urgency**: AI tagging.

### 🖐️ Action & Safety
- [x] **AI Composer**: Draft generation.
- [x] **Valve & Vault**: Safety gateway & encryption.
- [x] **Smart Attachments**: Context unlocking.

### 🤯 The Mind
- [x] **Strategist**: Archive/Reply decision engine.
- [x] **Context Builder**: Prompt assembly.
- [x] **Gemini 2.0**: LLM Gateway.

### 👮 HITL & Admin
- [x] **Escalation Queue**: Human review workflow.
- [x] **Kill Switch**: Global safety halt.
- [x] **Billing**: Stripe integration.

### 🚪 Public Gateway
- [x] **Landing Page**: Marketing site (V0).
- [x] **Onboarding**: Signup wizard (V0).

## 4. Strategic Recommendation
To fix the "Deployment" issue, we must **NOT** just build more features. We must implement the **Governance Primitives** first.

1.  **Step 1: Define the Deployment Readiness Contract (DRC).**
2.  **Step 2: Define the Vertical Slice Mandate.**
3.  **Step 3: Execute the "Email Reply v0" Vertical Slice** (stubbing everything else).

## 5. Critical Findings (Phase 1 Audit)
**Date**: 2026-02-12
**Status**: IMMEDIATE ACTION REQUIRED

### 🚨 CRITICAL: Tenant Isolation Starvation Bug
**Severity**: High (Data Leak / Denial of Service)
**Component**: `spine.chapters.intelligence.processor` / `spine.db.models.Email`

**The Vulnerability**:
The `Email` database table lacks a `tenant_id` column. It keys off `provider_message_id`.
In `processor.py`:
```python
stmt = select(Email).where(Email.provider_message_id == triage_result.message_id)
# ...
if existing_email:
    continue # SKIPS WORK ITEM CREATION
```

**The Scenario**:
1. User A (Tenant 1) receives Email X (Message-ID: 123). Processor saves it.
2. User B (Tenant 2) receives forwarded Email X (Message-ID: 123) or imports same account.
3. Processor sees `Message-ID: 123` exists.
4. Processor **SKIPS** creating a WorkItem for Tenant 2.
5. **Result**: Tenant 2 never sees the email.

**Corrective Action**:
1. **Schema**: Add `tenant_id` to `Email` table OR enforce 1:1 `Email` <-> `WorkItem` relation strictly scoped.
2. **Logic**: Query must be `select(Email).where(Email.provider_message_id == ...).where(Email.tenant_id == tx_id)`.
