# Chapter 09: Observability (CloudWatch)

## Purpose
To provide centralized logging, metrics, and dashboards for the application.

## Context
"Phase 1: Infrastructure."
- **CloudWatch Logs**: Centralized logs for API, Workers, and System.
- **CloudWatch Dashboards**: High-level view of system health.

## Requirements
1.  **Log Groups**:
    - `/aws/ecs/assistants-api`
    - `/aws/lambda/assistants-worker`
2.  **Retention**: 30 Days.
3.  **Dashboard**: Basic "Overview" dashboard placeholder.

## Verification
1.  `terraform validate`.
2.  Visual Report showing Log Group creation.
