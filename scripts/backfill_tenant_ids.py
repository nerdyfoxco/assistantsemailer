
import asyncio
import uuid
import logging
import sys
from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Adjust path to find spine modules
import sys
import os
sys.path.append(os.getcwd())

from spine.core.config import settings
from spine.db.models import Email, WorkItem

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("backfill_tenant_ids")

# Database Setup
DATABASE_URL = "sqlite+aiosqlite:///./spine.db"
logger.info(f"Using Database: {DATABASE_URL}")

engine = create_async_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def backfill_emails():
    async with SessionLocal() as session:
        logger.info("Starting Backfill: Tenant IDs on Emails...")
        
        # 1. Find Emails with NULL tenant_id
        stmt = select(Email).where(Email.tenant_id.is_(None))
        result = await session.execute(stmt)
        emails = result.scalars().all()
        
        logger.info(f"Found {len(emails)} emails with missing tenant_id.")
        
        processed = 0
        splits = 0
        orphans = 0
        
        for email in emails:
            # 2. Find associated WorkItems
            wi_stmt = select(WorkItem.tenant_id).where(WorkItem.email_id == email.id).group_by(WorkItem.tenant_id)
            wi_result = await session.execute(wi_stmt)
            tenant_ids = wi_result.scalars().all()
            
            if not tenant_ids:
                logger.warning(f"Email {email.id} has NO WorkItems. Marking as Orphan.")
                # Strategy: Assign to null/default or delete? 
                # For safety, we leave it NULL or assign a placeholder? 
                # Protocol says "Derived tenant via WorkItem relation".
                # If no relation, we can't derive.
                orphans += 1
                continue
                
            if len(tenant_ids) == 1:
                # Safe Update
                email.tenant_id = tenant_ids[0]
                session.add(email)
                processed += 1
                
            else:
                # COLLISION DETECTED
                logger.warning(f"COLLISION: Email {email.id} shared by tenants {tenant_ids}. Splitting...")
                
                # Assign original to First Tenant
                first_tenant = tenant_ids[0]
                email.tenant_id = first_tenant
                session.add(email)
                processed += 1
                
                # Clone for others
                for other_tenant in tenant_ids[1:]:
                    new_id = str(uuid.uuid4())
                    logger.info(f"  -> Cloning {email.id} to {new_id} for tenant {other_tenant}")
                    
                    new_email = Email(
                        id=new_id,
                        tenant_id=other_tenant,
                        provider_message_id=email.provider_message_id,
                        thread_id=email.thread_id,
                        from_email=email.from_email,
                        to_emails=email.to_emails,
                        cc_emails=email.cc_emails,
                        subject=email.subject,
                        received_at=email.received_at,
                        gmail_id=email.gmail_id,
                        snippet=email.snippet,
                        body_text=email.body_text,
                        body_html=email.body_html,
                        is_read=email.is_read,
                        direction=email.direction
                    )
                    session.add(new_email)
                    splits += 1
                    
                    # Update WorkItems for this tenant to point to NEW Email
                    # We need to find WorkItems for this email AND this tenant
                    update_wi_stmt = select(WorkItem).where(
                        WorkItem.email_id == email.id,
                        WorkItem.tenant_id == other_tenant
                    )
                    wi_to_update = (await session.execute(update_wi_stmt)).scalars().all()
                    
                    for wi in wi_to_update:
                        wi.email_id = new_id
                        session.add(wi)
        
        await session.commit()
        logger.info(f"Backfill Complete. Processed: {processed}, Splits: {splits}, Orphans: {orphans}")

if __name__ == "__main__":
    asyncio.run(backfill_emails())
