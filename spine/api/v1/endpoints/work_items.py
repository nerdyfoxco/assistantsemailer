from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from spine.api.deps import get_db, get_current_user
from spine.services.workflow_service import WorkflowService
from spine.repositories.work_item_repo import WorkItemRepository
from spine.repositories.tenant_repo import TenantRepository
from spine.repositories.email_repo import EmailRepository
from spine.db.models import User, WorkItemState, WorkItem
# from spine.contracts.common import WorkItemResponse
from pydantic import BaseModel

router = APIRouter()

# Response Model (Move to contracts if needed, but defining here for speed)
# Ideally this should be in spine/contracts/common.py or work_items.py

class WorkItemOut(BaseModel):
    id: str
    tenant_id: str
    email_id: str
    state: str
    priority: int
    tags: List[str]
    created_at: str
    # Add other fields as needed

    class Config:
        from_attributes = True

# We need a service instance. 
# Dependency injection for Service
async def get_workflow_service(db: AsyncSession = Depends(get_db)) -> WorkflowService:
    try:
        print("DEBUG: Initializing WorkflowService dependency")
        work_item_repo = WorkItemRepository(db)
        service = WorkflowService(work_item_repo)
        print("DEBUG: WorkflowService created")
        return service
    except Exception as e:
        print(f"ERROR: Failed to create WorkflowService: {e}")
        import traceback
        traceback.print_exc()
        raise e

from fastapi import Response, Request

@router.options("/", include_in_schema=False)
async def options_work_items(request: Request):
    response = Response()
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response

@router.get("/", response_model=List[WorkItemOut])
async def list_work_items(
    state: Optional[WorkItemState] = None,
    current_user: User = Depends(get_current_user),
    service: WorkflowService = Depends(get_workflow_service)
):
    """
    List work items, optionally filtered by state.
    """
    # Using the repo directly for listing might be easier if service doesn't have a list method
    # Let's check service... It has create and transition.
    # We should add a list method to service or repo.
    # Repo has `get_by_state`.
    
    try:
        print(f"Listing work items. State: {state}, User: {current_user.email}")
        
        if state:
            items = await service.repo.get_by_state(state)
        else:
            # Fallback to getting all? Repo doesn't have get_all.
            # Let's just return empty list or implement get_all in repo if needed.
            # For now, let's just return NEEDS_REPLY which is the default interesting state.
            items = await service.repo.get_by_state(WorkItemState.NEEDS_REPLY)
            # TODO: Implement get_all in repo

        print(f"Found {len(items)} items")
            
        # Simple conversion for now to avoid validation errors with datetime strings etc
        return [
            WorkItemOut(
                id=item.id,
                tenant_id=item.tenant_id,
                email_id=item.email_id,
                state=item.state.value,
                priority=99, # Default priority as not in model yet
                tags=[], # Default tags as not in model yet
                created_at=item.created_at.isoformat()
            ) for item in items
        ]
    except Exception as e:
        print(f"ERROR listing work items: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{item_id}/transition", response_model=WorkItemOut)
async def transition_work_item(
    item_id: str,
    new_state: WorkItemState,
    current_user: User = Depends(get_current_user),
    service: WorkflowService = Depends(get_workflow_service)
):
    """
    Transition a work item to a new state.
    """
    item = await service.transition_state(item_id, new_state, actor_id=current_user.id)
    if not item:
        raise HTTPException(status_code=404, detail="Work item not found")
    
    await service.repo.session.commit() # Ensure it persists
    await service.repo.session.refresh(item)
    
    return WorkItemOut(
        id=item.id,
        tenant_id=item.tenant_id,
        email_id=item.email_id,
        state=item.state.value,
        priority=item.priority,
        tags=item.tags,
        created_at=item.created_at.isoformat()
    )
