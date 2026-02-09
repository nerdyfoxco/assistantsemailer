from typing import List
from sqlalchemy import select
from spine.db.models import Email
from spine.db.repository import BaseRepository

class EmailRepository(BaseRepository[Email]):
    async def get_by_provider_message_id(self, provider_message_id: str) -> Email | None:
        result = await self.session.execute(select(Email).where(Email.provider_message_id == provider_message_id))
        return result.scalar_one_or_none()

    async def get_by_thread_id(self, thread_id: str) -> List[Email]:
        result = await self.session.execute(select(Email).where(Email.thread_id == thread_id))
        return list(result.scalars().all())
