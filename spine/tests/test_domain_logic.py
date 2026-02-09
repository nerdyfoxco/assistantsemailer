import pytest
import uuid
from datetime import datetime
from spine.db.database import AsyncSessionLocal
from spine.repositories.tenant_repo import TenantRepository
from spine.repositories.email_repo import EmailRepository
from spine.services.email_service import EmailService
from spine.db.models import Tenant, TenantPlan, Direction

@pytest.mark.asyncio
async def test_tenant_creation():
    async with AsyncSessionLocal() as session:
        repo = TenantRepository(Tenant, session)
        t_id = f"t_{uuid.uuid4()}"
        tenant = await repo.create(
            id=t_id,
            name="Acme Corp",
            plan=TenantPlan.PRO
        )
        await session.commit()
        
        fetched = await repo.get_by_id(t_id)
        assert fetched is not None
        assert fetched.name == "Acme Corp"
        assert fetched.plan == TenantPlan.PRO

@pytest.mark.asyncio
async def test_email_ingestion_idempotency():
    async with AsyncSessionLocal() as session:
        repo = EmailRepository(None, session) # Helper won't use model param for creation in service if svc handles it? 
        # Wait, BaseRepository needs model.
        repo = EmailRepository(None, session) 
        # Actually EmailService uses EmailRepository which inherits BaseRepository[Email]
        # We need to construct it correctly.
        
        # Correct construction
        from spine.db.models import Email
        email_repo = EmailRepository(Email, session)
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
            direction=Direction.INBOUND
        )
        await session.commit()
        
        # Second Ingestion (Duplicate)
        email2 = await service.ingest_email(
            provider_message_id=msg_id,
            thread_id="th_123",
            from_email="sender@example.com",
            to_emails="me@example.com",
            subject="Hello",
            received_at=datetime.utcnow(),
            direction=Direction.INBOUND
        )
        
        assert email1.id == email2.id
