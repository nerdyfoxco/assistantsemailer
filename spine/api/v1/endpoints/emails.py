from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from spine.db.database import get_db
from spine.api.deps import get_current_user
from spine.db.models import User
from spine.services.gmail_service import GmailService
from spine.repositories.email_repo import EmailRepository

router = APIRouter()

def get_gmail_service(db: AsyncSession = Depends(get_db)) -> GmailService:
    return GmailService(EmailRepository(db))

@router.post("/sync")
async def sync_emails(
    current_user: User = Depends(get_current_user),
    service: GmailService = Depends(get_gmail_service)
):
    """Triggers a manual sync of recent emails from Gmail."""
    try:
        count = await service.fetch_recent_threads(current_user.id)
        return {"message": "Sync complete", "emails_processed": count}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"SYNC ERROR: {e}")
        raise HTTPException(status_code=500, detail="Failed to sync emails")

@router.get("/")
async def list_emails(
    current_user: User = Depends(get_current_user),
    service: GmailService = Depends(get_gmail_service)
):
    """Returns recent emails for the user."""
    emails = await service.email_repo.get_recent_emails(limit=50)
    # Simple serialization
    return [
        {
            "id": e.id,
            "subject": e.subject,
            "from": e.from_email,
            "snippet": e.snippet,
            "received_at": e.received_at,
            "gmail_id": e.gmail_id
        }
        for e in emails
    ]
