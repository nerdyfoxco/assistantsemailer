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
        "http://localhost:3006",
        "http://127.0.0.1:3006",
    ]

    # SECURITY
    SECRET_KEY: str = "YOUR_SECRET_KEY"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30 * 24 * 8 # 8 days

    model_config = SettingsConfigDict(case_sensitive=True)

settings = Settings()
