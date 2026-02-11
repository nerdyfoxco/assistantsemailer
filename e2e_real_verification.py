
import asyncio
import logging
import sys
from spine.db.models import User, EmailAccount, Email, WorkItem
from spine.db.database import AsyncSessionLocal
from spine.core.config import settings
from spine.repositories.email_repo import EmailRepository
from spine.chapters.intelligence.streamer import GmailStreamer
from spine.chapters.intelligence.processor import IntelligenceProcessor
from spine.chapters.action.vault import Vault
from spine.chapters.action.unlocker import AttachmentUnlocker
from sqlalchemy import select

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("e2e_verifier")

# THE USER WE FOUND WITH A TOKEN
TARGET_USER_ID = "4b3c83b2-d1a9-435a-ac50-1520bc88ea4a"

async def verify_real_pipeline():
    print(f"\n=== E2E REAL DATA VERIFICATION: USER {TARGET_USER_ID} ===")
    
    async with AsyncSessionLocal() as session:
        # 1. SETUP COMPONENTS
        repo = EmailRepository(session)
        streamer = GmailStreamer(repo)
        processor = IntelligenceProcessor(session) # Uses repo internally if properly instantiated, or passed session
        vault = Vault(session)
        unlocker = AttachmentUnlocker(vault)
        
        # Verify Connectivity
        try:
            account = await repo.get_account_by_user(TARGET_USER_ID)
            print(f"-> ACCOUNT: {account.provider} (Token: {len(account.oauth_token_ref)} chars)")
        except Exception as e:
            print(f"!! FAILURE: Could not load account: {e}")
            return

        # 2. STREAM & PROCESS ONE THREAD (LIVE)
        print("\n[STEP 1] STREAMING LIVE GMAIL THREAD...")
        metrics = await processor.process_user_stream(TARGET_USER_ID, limit=1)
        print(f"-> METRICS: {metrics}")
        
        if metrics.get("errors") > 0:
            print("!! WARNING: Errors occurred during processing !!")
            
        if metrics.get("processed") == 0 and metrics.get("skipped_existing") == 0:
             print("!! WARNING: No threads processed. Inbox might be empty or caught up.")
        else:
             print("-> SUCCESS: Streamer connected and fetched data.")

        # 3. VERIFY PERSISTENCE (DB READ)
        print("\n[STEP 2] VERIFYING DB PERSISTENCE...")
        # Get the latest email
        stmt = select(Email).order_by(Email.received_at.desc()).limit(1)
        result = await session.execute(stmt)
        latest_email = result.scalars().first()
        
        if latest_email:
            print(f"-> LATEST EMAIL SAVED: '{latest_email.subject}'")
            print(f"   From: {latest_email.from_email}")
            print(f"   Received: {latest_email.received_at}")
        else:
            print("!! FAILURE: No emails found in DB !!")

        # 4. VERIFY WORK ITEM CREATION
        print("\n[STEP 3] VERIFYING INTELLIGENCE (WORK ITEMS)...")
        if latest_email:
            stmt = select(WorkItem).where(WorkItem.email_id == latest_email.id)
            result = await session.execute(stmt)
            wi = result.scalars().first()
            if wi:
                print(f"-> WORK ITEM CREATED: State={wi.state} | Confidence={wi.confidence_band}")
            else:
                print("!! FAILURE: Email saved but no WorkItem created !!")

        # 5. VERIFY VAULT (REAL ENCRYPTION)
        print("\n[STEP 4] VERIFYING VAULT & UNLOCKER...")
        test_key = "e2e_test_key"
        test_val = "secret_access_code_999"
        
        # Store
        await vault.stored_set(TARGET_USER_ID, test_key, test_val)
        
        # Retrieve
        retrieved = await vault.stored_get(TARGET_USER_ID, test_key)
        
        if retrieved == test_val:
            print(f"-> VAULT CHECK: PASS (Stored & Retrieved '{test_key}')")
        else:
            print(f"!! VAULT FAILURE: Mismatch !!")
            
        # Cleanup
        await vault.stored_delete(TARGET_USER_ID, test_key)

    print("\n=== E2E VERIFICATION COMPLETE ===")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(verify_real_pipeline())
