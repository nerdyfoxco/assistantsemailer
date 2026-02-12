
import asyncio
import logging
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Database Setup
DATABASE_URL = "sqlite+aiosqlite:///./spine.db" 
engine = create_async_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("cleanup_migration_tmp")

async def cleanup():
    async with SessionLocal() as session:
        logger.info("Dropping _alembic_tmp_emails table...")
        await session.execute(text("DROP TABLE IF EXISTS _alembic_tmp_emails"))
        await session.commit()
        logger.info("Dropped.")

if __name__ == "__main__":
    asyncio.run(cleanup())
