from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from spine.core.config import settings

# For now, ease of use: If Config has DB url use it, else default to local sqlite
# In prod this comes from env vars
DATABASE_URL = "sqlite+aiosqlite:///./spine.db"

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
