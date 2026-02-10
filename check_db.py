import asyncio
from sqlalchemy import select
from spine.db.database import AsyncSessionLocal
from spine.db.models import User, WorkItem

async def check_data():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User))
        users = result.scalars().all()
        print(f"Users found: {len(users)}")
        for u in users:
            print(f" - {u.email} ({u.id})")

        result = await session.execute(select(WorkItem))
        items = result.scalars().all()
        print(f"WorkItems found: {len(items)}")

if __name__ == "__main__":
    asyncio.run(check_data())
