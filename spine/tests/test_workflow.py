import pytest
import uuid
from datetime import datetime
from spine.db.models import WorkItem, WorkItemState, ConfidenceBand, Tenant, TenantPlan, Email, Direction, EmailProvider
from spine.repositories.work_item_repo import WorkItemRepository
from spine.services.workflow_service import WorkflowService
from spine.db.database import AsyncSessionLocal

@pytest.mark.asyncio
async def test_workflow_transitions():
    async with AsyncSessionLocal() as session:
        # 1. Setup Deps (Tenant, Email)
        t_id = f"t_{uuid.uuid4()}"
        session.add(Tenant(id=t_id, name="Workflow Corp", plan=TenantPlan.PRO))
        
        e_id = f"e_{uuid.uuid4()}"
        session.add(Email(
            id=e_id, 
            provider_message_id=str(uuid.uuid4()), 
            thread_id="th_wf", 
            from_email="a@b.com", 
            received_at=datetime.utcnow(), 
            direction=Direction.INBOUND
        ))
        await session.commit()
        
        # 2. Create WorkItem
        repo = WorkItemRepository(WorkItem, session)
        service = WorkflowService(repo)
        
        w_id = f"w_{uuid.uuid4()}"
        item = await service.create_work_item(
            id=w_id,
            tenant_id=t_id,
            email_id=e_id,
            confidence=ConfidenceBand.HIGH
        )
        await session.commit()
        
        assert item.state == WorkItemState.NEEDS_REPLY
        assert item.resolution_lock is False
        
        # 3. Transition to DONE
        updated = await service.transition_state(w_id, WorkItemState.DONE, actor_id="user_1")
        await session.commit()
        
        assert updated.state == WorkItemState.DONE
        assert updated.resolution_lock is True
        assert updated.closed_at is not None
