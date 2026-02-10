from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from spine.db.models import Email, EmailAccount, Direction, User
from spine.db.repository import BaseRepository
from typing import List, Optional
from datetime import datetime
import uuid

class EmailRepository(BaseRepository[Email]):
    def __init__(self, session: AsyncSession):
        super().__init__(Email, session)

    async def get_by_gmail_id(self, gmail_id: str) -> Optional[Email]:
        stmt = select(Email).where(Email.gmail_id == gmail_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def create_or_update(self, email_data: dict) -> Email:
        """
        Upserts an email based on gmail_id.
        """
        gmail_id = email_data.get("gmail_id")
        existing_email = await self.get_by_gmail_id(gmail_id)
        
        if existing_email:
            # Update fields if necessary (e.g. is_read status change?)
            # For now, we assume immutability of content, maybe just update flags
            # existing_email.is_read = email_data.get("is_read", existing_email.is_read)
            return existing_email
        
        # Create new
        new_email = Email(
            id=str(uuid.uuid4()),
            gmail_id=gmail_id,
            thread_id=email_data.get("thread_id"),
            provider_message_id=email_data.get("provider_message_id"),
            from_email=email_data.get("from_email"),
            to_emails=email_data.get("to_emails"), # JSON string
            cc_emails=email_data.get("cc_emails"),
            subject=email_data.get("subject"),
            snippet=email_data.get("snippet"),
            body_text=email_data.get("body_text"),
            received_at=email_data.get("received_at"),
            direction=email_data.get("direction", Direction.INBOUND),
            is_read=email_data.get("is_read", False)
        )
        self.session.add(new_email)
        # Session commit is handled by Service or UOW usually, but BaseRepository might not have explicit commit
        # We will let the service handle commit to batch operations if needed.
        return new_email

    async def get_recent_emails(self, limit: int = 50) -> List[Email]:
        stmt = select(Email).order_by(Email.received_at.desc()).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_account_by_user(self, user_id: str) -> Optional[EmailAccount]:
        # Helper to get the linked account credentials
        stmt = select(EmailAccount).where(EmailAccount.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()
