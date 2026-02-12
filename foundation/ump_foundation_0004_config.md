
# UMP-FOUNDATION-0004: System Configuration

**Module**: `foundation.config`
**Type**: **New Capability**
**Phase**: Phase 0 (Foundation)
**Depends On**: `pydantic-settings`

## 1. Objective
Establish a centralized, strong-typed configuration system using `pydantic-settings`. This allows configuration to be loaded from Environment Variables, `.env` files, or Secrets Managers (future), with validation at startup.

## 2. Proposed Interface

### A. Base Settings (`foundation.config.settings`)
```python
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Literal

class GlobalSettings(BaseSettings):
    """
    Root settings for the Foundation.
    All specific module settings should inherit or be nested here.
    """
    ENV: Literal["dev", "test", "prod"] = "dev"
    PROJECT_NAME: str = "assistants-co-system"
    TENANT_ID: str = "default"
    
    # Feature Flags (Code-as-Config for Phase 0)
    ENABLE_AUTHORITY_CHECKS: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

class DatabaseSettings(BaseSettings):
    DATABASE_URL: str
    POOL_SIZE: int = 5
    MAX_OVERFLOW: int = 10
```

## 3. Implementation Plan
1.  **Create** `foundation/config/settings.py`.
2.  **Test** `foundation/tests/test_config.py`.

## 4. Verification
*   **Unit Test**: Load settings from dummy env vars and verify types.
*   **Invariant**: `ENV` must default to `dev`.

## 5. Definition of Done
*   [ ] Modules created.
*   [ ] 100% Test Coverage.
