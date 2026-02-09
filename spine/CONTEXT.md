# Backend Core Context

## Purpose
The `spine` directory contains the core Python backend service. It serves as the API Gateway, Business Logic Layer, and Integration Hub for the Email System.

## Architecture
- **Framework**: FastAPI (Async).
- **Package Manager**: Poetry (using `pyproject.toml`).
- **Structure**:
    - `api/`: Route handlers.
    - `core/`: Config, Security, Logging.
    - `domain/`: Business logic.
    - `main.py`: App Entrypoint.

## Governance
- All code must be typed (`mypy` strict).
- All routes must return `pydantic` models.
- No direct database access in routes (use Service layer).
