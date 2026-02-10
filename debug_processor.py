import asyncio
import os
import sys
from sqlalchemy import select
from tabulate import tabulate

# Add workspace root to path
sys.path.append(os.getcwd())

from spine.db.database import get_db, AsyncSessionLocal
from spine.chapters.intelligence.processor import IntelligenceProcessor
from spine.db.models import WorkItem, Email, User
from spine.repositories.user_repo import UserRepository

async def main():
    print("=== UMP-50-05: Processor Visual Seal ===")
    
    async with AsyncSessionLocal() as db:
        # 1. Get Real User
        # Use simple select on User model
        result = await db.execute(select(User))
        user = result.scalars().first()
        
        if not user:
            print("❌ No user found in DB. Please run setup or login first.")
            return

        print(f"🔹 Running Processor for User: {user.email} ({user.id})")

        # 2. Initialize Processor
        processor = IntelligenceProcessor(db)

        # 3. Run Stream (Live from Gmail)
        print("🔹 Streaming & Processing (Limit=5)...")
        try:
            metrics = await processor.process_user_stream(user.id, limit=5)
            print(f"✅ Processor Finished. Metrics: {metrics}")
        except Exception as e:
            print(f"❌ Processor Failed: {e}")
            import traceback
            traceback.print_exc()
            return

        # 4. Verify Persistence (Query DB)
        print("\n🔹 Verifying Database Records:")
        
        # Check WorkItems - Join with Email to get subject
        stmt = select(WorkItem, Email).join(Email, WorkItem.email_id == Email.id).order_by(WorkItem.created_at.desc()).limit(10)
        rows = await db.execute(stmt)
        
        table_data = []
        for wi, email in rows:
            table_data.append([
                wi.state.value,
                wi.confidence_band.value,
                (email.subject or "")[:30],
                email.from_email,
                wi.created_at.strftime("%H:%M:%S")
            ])
            
        if table_data:
            print(tabulate(table_data, headers=["State", "Confidence", "Subject", "From", "Created"], tablefmt="grid"))
        else:
            print("⚠️ No WorkItems found in DB (Did the stream find new emails?)")

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
