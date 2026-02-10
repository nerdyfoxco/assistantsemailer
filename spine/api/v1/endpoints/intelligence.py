from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse, Response
from sqlalchemy.orm import Session
from typing import AsyncGenerator
import json
import asyncio

from spine.api import deps
from spine.core.config import settings
from spine.chapters.intelligence.streamer import GmailStreamer
from spine.chapters.intelligence.triage import triage_thread
from spine.chapters.intelligence.proxy import LiveProxy
from spine.services.gmail_service import GmailService
from spine.db.models import User

router = APIRouter()

@router.get("/stream")
async def stream_intelligence(
    limit: int = 10,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    """
    SSE Endpoint: Streams triaged work items from Gmail.
    Zero-Storage: Data flows from Gmail -> Triage -> Browser.
    """
    
    try:
        # 1. Init Services
        # We need the user's Gmail credentials. 
        # The GmailService usually handles this via 'creds' logic.
        # But GmailStreamer expects 'creds'.
        
        # Let's get the creds from GmailService helper (assuming it exists or we build it)
        from spine.repositories.email_repo import EmailRepository
        email_repo_svc = EmailRepository(db) # Use distinct name to avoid conflict with inner function var
        gmail_service = GmailService(email_repo_svc)
        creds = await gmail_service.get_user_credentials(current_user.id)
        
        if not creds:
             raise HTTPException(status_code=400, detail="Gmail not connected")
    
        # 2. Define Generator
        async def event_generator() -> AsyncGenerator[str, None]:
            from spine.repositories.email_repo import EmailRepository
            email_repo = EmailRepository(db)
            streamer = GmailStreamer(email_repo)
            
            # Initial Event: Connected
            yield f"data: {json.dumps({'type': 'connected'})}\n\n"
            
            try:
                # Yield from streamer
                async for thread_data in streamer.stream_recent_threads(
                    user_id=str(current_user.id),
                    limit=limit
                ):
                    # Triage
                    triage_result = triage_thread(thread_data)
                    
                    # Convert Pydantic to Dict for JSON
                    data = triage_result.model_dump()
                    # Add extra ID if needed
                    data['id'] = triage_result.thread_id
                    
                    # Yield SSE
                    yield f"data: {json.dumps(data, default=str)}\n\n"
                    
                    # Yield to event loop to allow heartbeat?
                    await asyncio.sleep(0.01)
                    
                # End Event
                yield f"data: {json.dumps({'type': 'done'})}\n\n"
                
            except Exception as e:
                yield f"data: {json.dumps({'error': str(e)})}\n\n"
    
        return StreamingResponse(event_generator(), media_type="text/event-stream")

    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response(content=f"Crash: {e}", status_code=500)

@router.get("/body/{message_id}")
async def get_message_body(
    message_id: str,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    """
    Fetches sanitized HTML body for a specific message.
    """
    from spine.repositories.email_repo import EmailRepository
    email_repo = EmailRepository(db)
    gmail_service = GmailService(email_repo)
    creds = await gmail_service.get_user_credentials(current_user.id)
    
    if not creds:
         raise HTTPException(status_code=400, detail="Gmail not connected")
         
    proxy = LiveProxy()
    try:
        result = await proxy.fetch_body(user_id="me", message_id=message_id, creds=creds)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
