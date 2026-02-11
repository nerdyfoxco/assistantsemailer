from fastapi import APIRouter
from spine.api.v1.endpoints import users, auth, work_items, emails

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(work_items.router, prefix="/work-items", tags=["work-items"])
api_router.include_router(emails.router, prefix="/emails", tags=["emails"])
from spine.api.v1.endpoints import intelligence, mind
api_router.include_router(intelligence.router, prefix="/intelligence", tags=["intelligence"])
api_router.include_router(mind.router, prefix="/mind", tags=["mind"])
