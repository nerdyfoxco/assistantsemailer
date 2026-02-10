import asyncio
import logging
from spine.db.database import AsyncSessionLocal
from spine.repositories.email_repo import EmailRepository
from spine.services.gmail_service import GmailService
from sqlalchemy import select
from spine.db.models import EmailAccount

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def sync_emails():
    logger.info("Starting Email Sync Worker...")
    async with AsyncSessionLocal() as session:
        email_repo = EmailRepository(session)
        gmail_service = GmailService(email_repo)
        
        # In a real worker, we'd query all email accounts. 
        # For this UMP, let's fetch all accounts and sync them.
        stmt = select(EmailAccount)
        result = await session.execute(stmt)
        accounts = result.scalars().all()
        
        logger.info(f"Found {len(accounts)} email accounts to sync.")
        
        for account in accounts:
            try:
                logger.info(f"Syncing User {account.user_id} (Provider: {account.provider})...")
                count = await gmail_service.fetch_recent_threads(account.user_id, limit=5)
                logger.info(f"  -> Synced {count} emails.")
            except Exception as e:
                logger.error(f"  -> Failed: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(sync_emails())
    except KeyboardInterrupt:
        pass
