
import logging
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from spine.core.config import settings
from spine.db.database import get_db
from spine.db.models import User, Email
from spine.api.deps import get_current_user
from spine.services.gmail_service import GmailService
from spine.repositories.email_repo import EmailRepository

from spine.chapters.mind.strategist import Strategist, Decision
from spine.chapters.mind.llm_client import LLMClient, GeminiLLMProvider, MockLLMProvider
from spine.chapters.mind.context import ContextBuilder

router = APIRouter()
logger = logging.getLogger(__name__)

# --- Dependencies ---
def get_strategist():
    # In a real app, these would be singletons or cached
    if settings.GEMINI_API_KEY:
        provider = GeminiLLMProvider(api_key=settings.GEMINI_API_KEY)
    else:
        provider = MockLLMProvider()
    
    llm = LLMClient(provider)
    context = ContextBuilder()
    return Strategist(llm, context)

def get_gmail_service(db: AsyncSession = Depends(get_db)):
    return GmailService(EmailRepository(db))

# --- Models ---
class ThinkRequest(BaseModel):
    force_refresh: bool = False

class ExecuteRequest(BaseModel):
    message_id: str
    decision: Decision

# --- Endpoints ---

@router.post("/think/{message_id}", response_model=Decision)
async def think_about_email(
    message_id: str,
    strategist: Strategist = Depends(get_strategist),
    current_user: User = Depends(get_current_user),
    service: GmailService = Depends(get_gmail_service)
):
    """
    Asks the AI to analyze an email and propose an action.
    message_id: Can be DB ID (UUID) or Gmail ID. We try both.
    """
    try:
        # 1. Fetch Email Object
        # Try finding by Gmail ID first as that's most common in context
        repo = service.email_repo
        email = await repo.get_by_gmail_id(message_id)
        
        # If not found, try by DB ID
        if not email:
            email = await repo.get(message_id)
            
        if not email:
            raise HTTPException(status_code=404, detail=f"Email {message_id} not found")

        # 2. Get Credentials for LiveProxy
        creds = await service.get_user_credentials(current_user.id)
        if not creds:
             raise HTTPException(status_code=400, detail="User has no linked Gmail account")

        # 3. Decide via Strategist
        decision = await strategist.decide(current_user.id, email, creds)
        return decision

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Think failed for {message_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/execute", status_code=202)
async def execute_decision(
    req: ExecuteRequest,
    current_user: User = Depends(get_current_user),
    service: GmailService = Depends(get_gmail_service)
):
    """
    Executes a decision (e.g. saves a draft, archives).
    """
    # Placeholder for now - just acknowledges
    return {"status": "queued", "action": req.decision.action}
