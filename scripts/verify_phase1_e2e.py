import sys
import os

# Add workspace root to sys.path
sys.path.append(os.getcwd())

from fastapi.testclient import TestClient
from fastapi import FastAPI
from chapters.api.router import router
from chapters.api.deps import get_container
from chapters.work.item import WorkItemState

def verify_vertical_slice():
    print(">>> Starting Phase 1 Vertical Slice Verification (Headless)...")
    
    # 1. Setup App
    app = FastAPI()
    app.include_router(router)
    client = TestClient(app)
    
    # Clean Store
    container = get_container()
    manager = container.work_manager
    manager._store.clear()
    
    print("[1] System Initialized. Store Empty.")

    # 2. Simulate Ingestion (Connector Layer)
    print("[2] Simulating Email Ingestion...")
    from chapters.connectors.gmail.service import EmailIngested
    event = EmailIngested(
        tenant_id="tenant_verification_1",
        message_id="msg_verify_001",
        snippet="Please help me with my order.",
        payload={}
    )
    
    # Manually trigger manager to simulate Event Bus delivery
    item = manager.handle_email_ingested(event)
    
    if not item:
        print("FAIL: Item not created from ingestion.")
        sys.exit(1)
        
    print(f"    Item Created: {item.id} [State: {item.state.value}]")

    # 3. List via API (Frontend View)
    print("[3] Verifying API List...")
    resp = client.get("/api/v2/work-items")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]['id'] == item.id
    print("    API returned correct item.")

    # 4. Trigger Draft (Brain)
    print("[4] Triggering AI Draft...")
    resp = client.post(f"/api/v2/work-items/{item.id}/draft")
    assert resp.status_code == 200
    
    # Refresh Item from Store
    item_refreshed = manager.get_item(item.id)
    print(f"    State after draft trigger: {item_refreshed.state.value}")
    
    if item_refreshed.state != WorkItemState.REVIEW:
        print("FAIL: Item did not move to REVIEW state.")
        sys.exit(1)
        
    print(f"    Draft Content: {item_refreshed.draft_context.get('body')}")

    # 5. Approve & Send (Action)
    print("[5] Approving Draft...")
    resp = client.post(f"/api/v2/work-items/{item.id}/approve")
    assert resp.status_code == 200
    
    item_final = manager.get_item(item.id)
    print(f"    State after approval: {item_final.state.value}")
    
    if item_final.state != WorkItemState.CLOSED:
        print("FAIL: Item did not move to CLOSED state.")
        sys.exit(1)

    print(">>> VERIFICATION SUCCESSFUL: Vertical Slice v0 is Operational.")

if __name__ == "__main__":
    verify_vertical_slice()
