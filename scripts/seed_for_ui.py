import sys
import os
import time
sys.path.append(os.getcwd())

from chapters.api.deps import get_container
from chapters.connectors.gmail.service import EmailIngested

def seed_inbox():
    print(">>> Seeding Inbox for UI Verification...")
    container = get_container()
    manager = container.work_manager
    manager._store.clear() # Start fresh

    # Seed 1: New Item
    event1 = EmailIngested(
        tenant_id="demo_tenant",
        message_id="msg_demo_001",
        snippet="Urgent: Proposal Review needed by 5pm",
        payload={"subject": "Proposal Review", "from": "boss@client.com"}
    )
    item1 = manager.handle_email_ingested(event1)
    print(f"    Seeded Item 1 (NEW): {item1.id} - {item1.source_message_id}")

    # Seed 2: Already Drafted (Review)
    event2 = EmailIngested(
        tenant_id="demo_tenant",
        message_id="msg_demo_002",
        snippet="Can we schedule a call?",
        payload={"subject": "Call Sync", "from": "peer@partner.com"}
    )
    item2 = manager.handle_email_ingested(event2)
    # Simulate Drafting
    from chapters.brain.service import BrainService
    brain = BrainService()
    brain.generate_draft(item2, "Casual") 
    print(f"    Seeded Item 2 (REVIEW): {item2.id} - {item2.source_message_id}")

    print(">>> Seeding Complete.")

if __name__ == "__main__":
    seed_inbox()
