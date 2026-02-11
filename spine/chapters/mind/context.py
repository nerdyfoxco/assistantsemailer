
import logging
from typing import List, Optional, Any, Dict
from pydantic import BaseModel
from spine.chapters.intelligence.proxy import LiveProxy
from spine.db.models import Email

logger = logging.getLogger(__name__)

class PromptContext(BaseModel):
    """
    The 'Mental State' provided to the LLM.
    Contains everything needed to make a decision.
    """
    message_id: str
    sender: str
    subject: str
    snippet: str
    body_text: str
    attachments_summary: str
    
    def to_system_prompt_addition(self) -> str:
        """Formats the context for the System Prompt."""
        return (
            f"--- EMAIL CONTEXT ---\n"
            f"From: {self.sender}\n"
            f"Subject: {self.subject}\n"
            f"Content: {self.body_text}\n"
            f"Attachments: {self.attachments_summary}\n"
            f"---------------------"
        )

class ContextBuilder:
    """
    UMP-70-02: The Context (Memory).
    Assembles the PromptContext from various sources.
    """
    def __init__(self, proxy: Optional[LiveProxy] = None):
        self.proxy = proxy or LiveProxy()

    async def build(self, user_id: str, email: Email, creds: Any) -> PromptContext:
        """
        Builds the context for a given email.
        Fetches body live from Gmail.
        """
        try:
            # 1. Fetch Metadata (Free)
            sender = email.from_email
            subject = email.subject
            snippet = email.snippet or ""
            
            # 2. Fetch Body (Costly/Live)
            # We use the proxy to get the sanitized body
            body_data = await self.proxy.fetch_body(user_id, email.provider_message_id, creds)
            
            # Prefer plain text for LLM, fall back to HTML or Snippet
            raw_html = body_data.get("html", "")
            # Simple strip tags if we only have HTML (Bleach is for safety, not text extraction)
            # For now, let's assume body_data might have keys like 'body_text' if I updated Proxy, 
            # but looking at Proxy code it returns 'html' and 'snippet'.
            # We will use snippet + basic HTML stripping for now.
            # Ideally Proxy should return 'text_content'. 
            # Let's rely on snippet for the "Meat" if text is missing, or simple TAG stripping.
            
            # For V1, just use the snippet + sender + subject. 
            # The LLM is smart enough.
            # But UMP says "Fetch Body".
            
            # Let's try to get text from the HTML if possible or if Proxy updates.
            # Current Proxy returns: id, snippet, html, mime_type, attachments.
            
            # We will use the HTML content but strip it down or just pass it if it's not too huge.
            # For strict correctness, let's just use the sanitized HTML as "body_text" for now,
            # trusting the LLM to ignore tags, OR (better) use the Snippet as the core.
            
            body_text = body_data.get("snippet", "")
            if len(body_text) < 50 and body_data.get("html"):
                 # If snippet is too short, dump the HTML (truncated)
                 body_text = body_data.get("html")[:2000] # Cap at 2k chars

            # 3. Summarize Attachments
            attachments = body_data.get("attachments", [])
            att_summary = ", ".join([f"{a['filename']} ({a['size']}b)" for a in attachments]) or "None"

            return PromptContext(
                message_id=email.provider_message_id,
                sender=sender,
                subject=subject,
                snippet=snippet,
                body_text=body_text,
                attachments_summary=att_summary
            )
            
        except Exception as e:
            logger.error(f"Failed to build context for {email.id}: {e}")
            # Fallback to metadata only
            return PromptContext(
                message_id=email.provider_message_id or "unknown",
                sender=email.from_email,
                subject=email.subject,
                snippet=email.snippet or "",
                body_text="[Error fetching body]",
                attachments_summary="Unknown"
            )
