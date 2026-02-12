import sys
import os
import json
sys.path.append(os.getcwd())

from chapters.connectors.gmail.service import GmailService
from chapters.brain.service import BrainService
from foundation.lib.logging import StructuredLogger

logger = StructuredLogger.get_logger("verify.real_world")

def verify_live_system():
    print(">>> Phase 3: Real World Verification (Live Data)")
    
    # 1. Check for Token
    if not os.path.exists("token.json"):
        print("!!! FAIL: 'token.json' missing. Run 'python scripts/auth_gmail.py' first.")
        sys.exit(1)

    with open("token.json", "r") as f:
        token_data = json.load(f)

    # 2. Initialize Real Services
    try:
        gmail = GmailService(tenant_id="live_user", token_data=token_data)
        brain = BrainService() # Configured with Real OpenAI
    except Exception as e:
        print(f"!!! FAIL: Service Init Failed: {e}")
        sys.exit(1)

    # 3. Fetch Real Emails
    print(">>> Step 1: Connecting to Gmail API...")
    try:
        threads = gmail.fetch_recent_threads(limit=3)
        print(f"    Fetched {len(threads)} threads.")
        if not threads:
            print("    WARN: Inbox Empty? Sending self-test email not implemented yet.")
    except Exception as e:
        print(f"!!! FAIL: Gmail Fetch Failed: {e}")
        sys.exit(1)

    # 4. Process One Thread
    if threads:
        target = threads[0]
        print(f">>> Step 2: Processing Thread '{target.subject}'")
        
        # 5. Generate Draft (Real AI)
        print(">>> Step 3: Brain Drafting (OpenAI)...")
        try:
            # Create a mock WorkItem wrapper for the real thread data
            from chapters.work.item import WorkItem, WorkItemState
            item = WorkItem(
                id="live_test_01",
                tenant_id="live_user",
                source_message_id=target.messages[-1].id, # Last message
                state="NEW",
                payload={"subject": target.subject, "from": "test@sender.com", "body": target.messages[-1].snippet} # Simplified
            )
            
            draft_text = brain.generate_draft(item, "Professional")
            print("    AI Draft Generated:")
            print(f"    --- START DRAFT ---\n{draft_text[:200]}...\n    --- END DRAFT ---")
        except Exception as e:
            print(f"!!! FAIL: Drafting Failed: {e}")
            sys.exit(1)

        print(">>> SUCCESS: Real World Loop Verified.")
        print("    (Gmail Connected -> Threads Fetched -> AI Drafted)")

if __name__ == "__main__":
    verify_live_system()
