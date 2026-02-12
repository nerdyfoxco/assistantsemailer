
import asyncio
import logging
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from spine.db.models import Email

# Database Setup
DATABASE_URL = "sqlite+aiosqlite:///./spine.db" # Default hardcoded for script
engine = create_async_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("cleanup_orphans")

async def cleanup():
    async with SessionLocal() as session:
        logger.info("Cleaning up orphans with NULL tenant_id...")
        
        # Delete emails where tenant_id is NULL
        stmt = delete(Email).where(Email.tenant_id.is_(None))
        result = await session.execute(stmt)
        await session.commit()
        
        logger.info(f"Deleted {result.rowcount} orphaned emails.")

if __name__ == "__main__":
    asyncio.run(cleanup())
