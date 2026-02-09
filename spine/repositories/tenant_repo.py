from sqlalchemy import select
from spine.db.models import Tenant
from spine.db.repository import BaseRepository

class TenantRepository(BaseRepository[Tenant]):
    async def get_by_name(self, name: str) -> Tenant | None:
        result = await self.session.execute(select(Tenant).where(Tenant.name == name))
        return result.scalar_one_or_none()
