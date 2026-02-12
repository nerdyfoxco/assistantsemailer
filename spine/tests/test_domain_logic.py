import pytest
import uuid
from datetime import datetime
from spine.db.database import AsyncSessionLocal
from spine.repositories.tenant_repo import TenantRepository
from spine.repositories.email_repo import EmailRepository
from spine.services.email_service import EmailService
from spine.db.models import Tenant, TenantPlan, Direction

@pytest.mark.asyncio
async def test_tenant_creation(db_session):
    repo = TenantRepository(Tenant, db_session)
    t_id = f"t_{uuid.uuid4()}"
    tenant = await repo.create(
        id=t_id,
        name="Acme Corp",
        plan=TenantPlan.PRO
    )
    # No manual commit needed if Repo commits. But BaseRepository usually commits.
    # If not, we might need it. BaseRepo usually does.
    
    fetched = await repo.get_by_id(t_id)
    assert fetched is not None
    assert fetched.name == "Acme Corp"
    assert fetched.plan == TenantPlan.PRO

@pytest.mark.asyncio
async def test_email_ingestion_idempotency(db_session):
    # Correct construction
    from spine.db.models import Email
    email_repo = EmailRepository(db_session)
    service = EmailService(email_repo)
    
    msg_id = f"gmail_{uuid.uuid4()}"
    
    # First Ingestion
    email1 = await service.ingest_email(
        provider_message_id=msg_id,
        thread_id="th_123",
        from_email="sender@example.com",
        to_emails="me@example.com",
        subject="Hello",
        received_at=datetime.utcnow(),
        direction=Direction.INBOUND,
        tenant_id="t_def" # PHASE 1.1: Fix Update
    )
    
    # Second Ingestion (Duplicate)
    email2 = await service.ingest_email(
        provider_message_id=msg_id,
        thread_id="th_123",
        from_email="sender@example.com",
        to_emails="me@example.com",
        subject="Hello",
        received_at=datetime.utcnow(),
        direction=Direction.INBOUND,
        tenant_id="t_def" # PHASE 1.1
    )
    
    # Should be same object/ID
    assert email1.id == email2.id
