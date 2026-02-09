# UMP-01-01: Execution Environment Baseline

## Purpose
To verify that the local execution environment satisfies the minimum requirements for the Assistants Co "Diamond Brick" protocol. This ensures that subsequent steps (Docker builds, AWS deploys, Python execution) do not fail due to missing primitives.

## Context
This is the "Physical Reality Check". Before we build the software, we must verify the factory.

## Requirements
1.  **OS**: Windows (PowerShell/WSL2 execution capable).
2.  **Runtime**: Python 3.10+, Node.js 18+.
3.  **Containerization**: Docker (Client/Daemon reachable).
4.  **Cloud**: AWS CLI v2 (configured or at least installed).
5.  **IaC**: Terraform 1.5+.
6.  **Browser**: Chrome/Edge (for Playwright visual verification).

## Output
- `env_report.html`: Visual proof of readiness.
- `env_status.json`: Machine-readable readiness.

## Guarantee
If this UMP passes, the agent allows itself to proceed to UMP-00-01 (Authority Contract).
