import uuid
from datetime import datetime
from typing import Optional
from spine.db.models import Email, Direction
from spine.repositories.email_repo import EmailRepository

class EmailService:
    def __init__(self, email_repo: EmailRepository):
        self.email_repo = email_repo

    async def ingest_email(
        self,
        provider_message_id: str,
        thread_id: str,
        from_email: str,
        to_emails: str,
        subject: str,
        received_at: datetime,
        direction: Direction,
        tenant_id: str, # PHASE 1.1: Tenant Isolation
        cc_emails: Optional[str] = None
    ) -> Email:
        # 1. Idempotency Check
        existing = await self.email_repo.get_by_provider_message_id(provider_message_id, tenant_id)
        if existing:
            return existing

        # 2. Create
        email = await self.email_repo.create(
            id=f"msg_{uuid.uuid4()}",
            tenant_id=tenant_id,
            provider_message_id=provider_message_id,
            thread_id=thread_id,
            from_email=from_email,
            to_emails=to_emails,
            cc_emails=cc_emails,
            subject=subject,
            received_at=received_at,
            direction=direction
        )
        await self.email_repo.session.flush() # Ensure ID is available if needed immediately
        # Note: We commit at the Controller/UnitOfWork level usually, but here we might trust the repo's session management
        # For this Service, we assume the session is managed externally or we should commit if this is atomic.
        # Given BaseRepository uses the passed session, the caller (Dependency Injection) handles commit.
        
        return email
