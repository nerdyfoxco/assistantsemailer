from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from spine.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"GLOBAL LOG: Request {request.method} {request.url}")
    try:
        response = await call_next(request)
        print(f"GLOBAL LOG: Response status {response.status_code}")
        return response
    except Exception as e:
        print(f"GLOBAL LOG: Exception {e}")
        import traceback
        traceback.print_exc()
        raise e

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False, # Allow * requires False
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi import Response

@app.options("/{full_path:path}")
async def options_handler(request: Request, full_path: str):
    print(f"Handling OPTIONS for {full_path}")
    response = Response()
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response

from spine.api.v1.api import api_router
from spine.api.v1.endpoints import auth
from spine.chapters.hitl.api import router as hitl_router
from spine.chapters.admin import admin_router
app.include_router(api_router, prefix=settings.API_V1_STR)
# The following routers are not defined in the original document, but are included as per the instruction.
# Assuming they are imported or defined elsewhere in the actual project context.
# If these are not defined, this will cause a NameError.
# app.include_router(users.router)
# app.include_router(mind_endpoints.router)
# app.include_router(intelligence_router)
app.include_router(hitl_router)
app.include_router(admin_router, prefix=settings.API_V1_STR)
# Mount Auth router at root for Google OAuth Callback compatibility
app.include_router(auth.router, prefix="/auth", tags=["auth"])

from spine.chapters.public.auth import router as public_auth_router
app.include_router(public_auth_router)

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

if __name__ == "__main__":
    import uvicorn
    import sys
    import os
    # Add parent dir to path
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    uvicorn.run(app, host="0.0.0.0", port=8000)
