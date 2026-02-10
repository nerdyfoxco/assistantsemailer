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
    SECRET_KEY: str = "79c2b4e85f0a1d369c8e2b7a4f1d5e9b0a8c7d6e5f4a3b2c1d0e9f8a7b6c5d4"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30 * 24 * 8 # 8 days

    # GOOGLE OAUTH
    GOOGLE_CLIENT_ID: str = "1055567309106-f58dlqu8c92vp5db6o5nufronlbvkjhv.apps.googleusercontent.com"
    GOOGLE_CLIENT_SECRET: str = "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"
    # Strict Backend Callback as requested
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/auth/google/callback"

    model_config = SettingsConfigDict(case_sensitive=True)

settings = Settings()
