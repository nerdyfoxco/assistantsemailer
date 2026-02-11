"""
UMP-50-05: The Processor (Assembler)
------------------------------------
Context: Orchestrates Streamer -> Triage -> DB (WorkItems).
Purpose: Persists triaged intelligence into the database as WorkItems.
Rules:
- Idempotent: Skips existing WorkItems (by email_id).
- Transactional: Commits in batches or per item safely.
- Zero-Body: Does NOT save email body (only metadata).
"""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from datetime import datetime
import logging
import uuid # Imported at top level

from spine.db.models import WorkItem, Email, EmailProvider, Direction, WorkItemState, ConfidenceBand
from spine.chapters.intelligence.streamer import GmailStreamer
from spine.chapters.intelligence.triage import triage_thread, TriageResult
from spine.repositories.email_repo import EmailRepository

logger = logging.getLogger(__name__)

class IntelligenceProcessor:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.email_repo = EmailRepository(db)
        self.streamer = GmailStreamer(self.email_repo)

    async def process_user_stream(self, user_id: str, limit: int = 10) -> dict:
        """
        Streams threads from Gmail, Triages them, and Persists new WorkItems.
        Returns metrics on processed count.
        """
        metrics = {
            "scanned": 0,
            "processed": 0,
            "skipped_existing": 0,
            "errors": 0
        }

        # 1. Get Tenant ID for the user
        account = await self.email_repo.get_account_by_user(user_id)
        if not account:
            logger.error(f"No email account found for user {user_id}")
            return metrics
        
        tenant_id = account.tenant_id

        try:
            # 2. Stream
            async for thread_data in self.streamer.stream_recent_threads(user_id, limit):
                metrics["scanned"] += 1
                
                try:
                    # 3. Triage
                    triage_result: TriageResult = triage_thread(thread_data)
                    
                    # 4. Idempotency Check
                    stmt = select(Email).where(Email.provider_message_id == triage_result.message_id)
                    result = await self.db.execute(stmt)
                    existing_email = result.scalars().first()

                    if existing_email:
                        metrics["skipped_existing"] += 1
                        continue

                    # 5. Persist (Email Meta + WorkItem)
                    await self._save_work_item(triage_result, tenant_id, user_id)
                    metrics["processed"] += 1
                    
                except Exception as e:
                    logger.error(f"Error processing thread {thread_data.get('id')}: {e}")
                    metrics["errors"] += 1
                    # Continue to next item

        except Exception as e:
            logger.critical(f"Fatal error in processor stream: {e}")
            raise e

        return metrics

    async def _save_work_item(self, meta: TriageResult, tenant_id: str, user_id: str):
        """
        Saves Email Metadata and linked WorkItem in a single transaction.
        """
        try:
            # A. Create Email Record (Metadata only)
            email_uuid = str(uuid.uuid4())

            email = Email(
                id=email_uuid,
                provider_message_id=meta.message_id,
                thread_id=meta.thread_id,
                from_email=meta.sender,
                subject=meta.subject,
                received_at=meta.received_at, # already datetime
                snippet=meta.snippet,
                direction=Direction.INBOUND,
                # Defaults
                to_emails=None,
                cc_emails=None,
                body_text=None,
                body_html=None,
                is_read=False
            )
            self.db.add(email)
            await self.db.flush() 

            # B. Create WorkItem
            wi = WorkItem(
                id=str(uuid.uuid4()),
                tenant_id=tenant_id,
                email_id=email.id,
                state=WorkItemState(meta.suggested_state.value), # Map Enum name
                owner_type="USER",
                owner_id=user_id,
                confidence_band=ConfidenceBand(meta.confidence.value),
                resolution_lock=False,
                created_at=datetime.utcnow()
            )
            self.db.add(wi)
            
            # C. Commit
            await self.db.commit()

        except IntegrityError:
            await self.db.rollback()
            # Race condition or duplicate
            logger.warning(f"Duplicate entry ignored for {meta.message_id}")
        except Exception as e:
            await self.db.rollback()
            raise e
