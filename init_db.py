import asyncio
from spine.db.database import engine
from spine.db.models import Base

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    print("Tables created.")

if __name__ == "__main__":
    asyncio.run(init_models())
