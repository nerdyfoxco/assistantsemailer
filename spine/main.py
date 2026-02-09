from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from spine.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

from spine.api.v1.api import api_router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/health", status_code=200)
def health_check():
    """
    Health Check Endpoint.
    """
    return {
        "status": "ok",
        "version": settings.VERSION,
        "project": settings.PROJECT_NAME
    }

@app.get("/")
def root():
    return {"message": "Welcome to Assistants Co Spine API"}
