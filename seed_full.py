import asyncio
import uuid
from datetime import datetime
from spine.db.database import AsyncSessionLocal as async_session_maker
from spine.db.models import Tenant, Email, WorkItem, WorkItemState, User, Direction, ConfidenceBand, Role, TenantMembership, TenantPlan
from spine.core.security import get_password_hash

async def seed_data():
    print("Starting seed_full.py execution...")
    async with async_session_maker() as session:
        # 0. Check if Admin exists
        # Ideally query, but for now we'll try to create and ignore unique violation if simpler, 
        # or just create a new one with random ID but specific email
        # We need specific email for login
        
        # 1. Create Tenant
        tenant_id = str(uuid.uuid4())
        tenant = Tenant(id=tenant_id, name="Demo Tenant", plan=TenantPlan.FREE) 
        session.add(tenant)
        
        # 2. Create User (Admin)
        user_id = str(uuid.uuid4())
        # Check if we can just upsert or something? 
        # Since we use SQLite/PG, we can try/except commit?
        # Let's just create it. If it fails due to email unique constraint, we'll assume it exists.
        
        admin_email = "admin@example.com"
        
        try:
            user = User(
                id=user_id,
                email=admin_email,
                hashed_password=get_password_hash("password123"),
                name="Admin User",
                created_at=datetime.utcnow()
            )
            session.add(user)
            
            # Link User to Tenant?
            membership = TenantMembership(
                id=str(uuid.uuid4()),
                tenant_id=tenant_id,
                user_id=user_id,
                role=Role.OWNER
            )
            session.add(membership)
            
        except Exception:
            print(f"User {admin_email} might already exist or failed.")

        # 3. Create Email
        email_id = str(uuid.uuid4())
        email = Email(
            id=email_id,
            provider_message_id=f"msg-{uuid.uuid4()}",
            thread_id=f"th-{uuid.uuid4()}",
            from_email="customer@example.com",
            to_emails="support@example.com",
            cc_emails=None,
            subject="Help needed with order",
            received_at=datetime.utcnow(),
            direction=Direction.INBOUND
        )
        session.add(email)
        
        # 4. Create WorkItem
        wi_id = str(uuid.uuid4())
        wi = WorkItem(
            id=wi_id,
            tenant_id=tenant_id,
            email_id=email_id,
            state=WorkItemState.NEEDS_REPLY,
            owner_type="USER",
            owner_id=user_id,
            confidence_band=ConfidenceBand.HIGH,
            resolution_lock=False,
            created_at=datetime.utcnow()
        )
        session.add(wi)
        
        try:
            await session.commit()
            print(f"Seeded: Tenant {tenant.name}, User {admin_email}, Email {email.subject}, WorkItem {wi.state}")
        except Exception as e:
            print(f"Commit failed: {e}")
            await session.rollback()

if __name__ == "__main__":
    try:
        asyncio.run(seed_data())
    except Exception as e:
        print(f"Seeding error: {e}")
