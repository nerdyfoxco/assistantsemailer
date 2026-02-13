# Verification Tasks: Fyxer Project

## Phase 1: Foundation & Identity
- [ ] Verify AWS CLI version matches requirements.
- [ ] Verify Docker version matches requirements.
- [ ] Check MFA enforcement on AWS root account.

## Phase 2: Core Infrastructure
- [ ] Verify VPC CIDR block (10.0.0.0/16).
- [ ] Verify Subnet isolation (Public vs Private).
- [ ] Verify EKS Cluster Status ('Active').

## Phase 3: Data & Storage
- [ ] Verify Postgres Connection (Auth, Host, Port).
- [ ] Verify Schema Existence (users, workflows, policies).
- [ ] Verify S3 Bucket access (List/Put permissions).

## Phase 4: Backend Core (Spine & Brain)
- [ ] Verify Brain Service Health (/healthz).
- [ ] Verify Spine Auth Logic (Login/Signup endpoints).
- [ ] Verify Workflow Creation (POST /v1/workflow/start).

## Phase 5: Integration Gateway (Ears)
- [ ] Verify Gmail Polling Loop (Logs).
- [ ] Verify Email Ingestion -> Workflow Event (Trace ID).
- [ ] Verify OAuth Token Refresh (Mock or Real).

## Phase 6: AI & Intelligence
- [ ] Verify LLM Generation (Mock or Real API Call).
- [ ] Verify Tone Analysis Output Format.
- [ ] Verify Context Classification Accuracy.

## Phase 7: Frontend Application (Face)
- [ ] **Browser Verification**:
    - [ ] Open Landing Page.
    - [ ] Navigate to Login.
    - [ ] Perform Signup Flow.
    - [ ] Connect Gmail Account (via OAuth UI).
    - [ ] View Dashboard (Inbox).
    - [ ] Edit Draft.
    - [ ] Approve Workflow.

## Phase 8: Deployment & Security
- [ ] Verify Secrets via Env Var Injection.
- [ ] Verify HTTPS Redirect (if deployed).
- [ ] Verify CI/CD Pipeline Success (GitHub Actions).
