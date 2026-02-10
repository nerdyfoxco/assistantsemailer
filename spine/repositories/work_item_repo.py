from typing import List
from sqlalchemy import select
from spine.db.models import WorkItem, WorkItemState
from spine.db.repository import BaseRepository

class WorkItemRepository(BaseRepository[WorkItem]):
    def __init__(self, session):
        super().__init__(WorkItem, session)

    async def get_by_state(self, state: WorkItemState) -> List[WorkItem]:
        result = await self.session.execute(select(WorkItem).where(WorkItem.state == state))
        return list(result.scalars().all())

    async def get_by_email_id(self, email_id: str) -> WorkItem | None:
        result = await self.session.execute(select(WorkItem).where(WorkItem.email_id == email_id))
        return result.scalar_one_or_none()
