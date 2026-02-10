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
app.include_router(api_router, prefix=settings.API_V1_STR)
# Mount Auth router at root for Google OAuth Callback compatibility
app.include_router(auth.router, prefix="/auth", tags=["auth"])

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
