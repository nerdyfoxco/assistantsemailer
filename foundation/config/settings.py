from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Literal

class GlobalSettings(BaseSettings):
    """
    Root settings for the Foundation.
    All specific configuration for Canonical modules should live here.
    This replaces `spine.core.config` for the Canonical/Foundation layer.
    """
    ENV: Literal["dev", "test", "prod"] = "dev"
    PROJECT_NAME: str = "assistants-co-system"
    TENANT_ID: str = "default"
    
    # Feature Flags (Code-as-Config for Phase 0)
    ENABLE_AUTHORITY_CHECKS: bool = True
    
    # Example config specific to Foundation Services
    REDIS_URL: str = "redis://localhost:6379/0"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        # We allow extra (ignore) because existing spine env files might have random keys
        extra="ignore",
        # Case insensitive parsing
        case_sensitive=False
    )
