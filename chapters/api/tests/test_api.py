import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from chapters.api.router import router
from chapters.api.deps import get_container
from chapters.work.item import WorkItem, WorkItemState

app = FastAPI()
app.include_router(router)

client = TestClient(app)

@pytest.fixture(autouse=True)
def cleanup_store():
    # Clear the singleton store before each test
    container = get_container()
    container.work_manager._store.clear()

def test_list_items_empty():
    response = client.get("/api/v2/work-items/")
    assert response.status_code == 200
    assert response.json() == []

def test_get_item_workflow():
    # 1. Manually inject an item into the manager (Simulate Ingestion)
    container = get_container()
    manager = container.work_manager
    brain = container.brain_service
    
    item = WorkItem("t1", "msg1", {"snippet": "Hi"})
    manager._store[item.id] = item

    # 2. Verify List finds it
    response = client.get("/api/v2/work-items/")
    assert len(response.json()) == 1
    assert response.json()[0]['id'] == item.id
    assert response.json()[0]['state'] == "NEW"

    # 3. Trigger Draft
    response = client.post(f"/api/v2/work-items/{item.id}/draft")
    assert response.status_code == 200
    
    # Note: Background tasks might not run instantly in TestClient without explicit handling 
    # or if we are just calling the function directly. 
    # But since we are using the simple non-async def for `generate_draft`, 
    # we might need to verify the side effect. 
    # FastAPI BackgroundTasks run *after* response. 
    # In tests, we can call the logic directly or wait.
    # Let's manually trigger the logic for deterministic test if needed, 
    # OR trust Starlette's TestClient to run background tasks (it usually does).
    
    # Check if state updated (Brain is synchronous mock)
    # Actually brain.generate_draft is sync, so it blocks the thread if called directly,
    # but as background task it runs after response.
    # We might need to refresh item state from store.
    
    # Let's simulate the immediate effect for the test by calling it directly 
    # if the background task didn't finish (race condition in tests).
    # But strictly, TestClient runs background tasks synchronously after the request.
    
    item_check = manager.get_item(item.id)
    assert item_check.state == WorkItemState.REVIEW
    assert item_check.draft_context is not None

    # 4. Approve
    response = client.post(f"/api/v2/work-items/{item.id}/approve")
    assert response.status_code == 200

    item_final = manager.get_item(item.id)
    assert item_final.state == WorkItemState.CLOSED
