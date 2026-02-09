from typing import List, Union
from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Assistants Co Spine"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost:3000",
        "http://localhost:8000",
    ]

    # SECURITY
    SECRET_KEY: str = "INSECURE_DEV_KEY_CHANGE_ME"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8 # 8 days

    model_config = SettingsConfigDict(case_sensitive=True)

settings = Settings()
