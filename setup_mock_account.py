import asyncio
import sys
from spine.db.database import AsyncSessionLocal
from spine.db.models import User, EmailAccount, EmailProvider, Tenant
from spine.core import security
from datetime import datetime
import uuid
import json

from sqlalchemy import text

async def setup_test_data():
    async with AsyncSessionLocal() as session:
        # 1. Get or Create User
        result = await session.execute(
            text("SELECT * FROM users WHERE email = 'agent_retry_2@example.com'")
        )
        user = result.fetchone()
        
        if not user:
            print("User not found, creating...")
            # Create Tenant first
            tenant_id = str(uuid.uuid4())
            await session.execute(
                text(f"INSERT INTO tenants (id, name, plan, created_at) VALUES ('{tenant_id}', 'Dev Tenant', 'FREE', '{datetime.utcnow()}')")
            )
            
            user_id = str(uuid.uuid4())
            await session.execute(
                text(f"INSERT INTO users (id, email, name, hashed_password, created_at) VALUES ('{user_id}', 'agent_retry_2@example.com', 'Agent', 'fakehash', '{datetime.utcnow()}')")
            )
            await session.commit()
            print(f"Created User {user_id}")
        else:
            user_id = user[0] # Tuple index 0 is id
            # Get tenant? assume one exist or we created earlier
            print(f"Found User {user_id}")

        # 2. Check/Create EmailAccount
        result = await session.execute(
             text(f"SELECT * FROM email_accounts WHERE user_id = '{user_id}'")
        )
        account = result.fetchone()
        
        if not account:
            print("Linking Mock Gmail Account...")
            # We need a tenant_id. Let's grab one.
            t_res = await session.execute(text("SELECT id FROM tenants LIMIT 1"))
            tenant_id = t_res.scalar()
            
            # Using FAKE credentials - this will fail actual Google API call if we don't mock it?
            # Correct. This script is to setup DB. The actual call needs valid creds OR we mock the service.
            # But wait, `POST /sync` calls real service.
            # So this script is only useful if we have real Access Token.
            # Attempting to use a placeholder.
            
            fake_tokens = {
                "access_token": "ya29.valid_token_placeholder", 
                "refresh_token": "refresh_token_placeholder",
                "scope": "https://www.googleapis.com/auth/gmail.readonly"
            }
            
            await session.execute(
                text(f"INSERT INTO email_accounts (id, tenant_id, user_id, provider, oauth_token_ref, created_at) VALUES ('{str(uuid.uuid4())}', '{tenant_id}', '{user_id}', 'GMAIL', '{json.dumps(fake_tokens)}', '{datetime.utcnow()}')")
            )
            await session.commit()
            print("Linked Mock Gmail Account.")
        else:
            print("Gmail Account already linked.")

        # 3. Seed Fake Emails
        print("Seeding fake emails...")
        from spine.db.models import Direction
        
        email_id_1 = str(uuid.uuid4())
        await session.execute(
            text(f"INSERT INTO emails (id, gmail_id, thread_id, provider_message_id, subject, from_email, snippet, received_at, direction, is_read) VALUES ('{email_id_1}', 'g1', 't1', 'msg1', 'Welcome to Fyxer', 'team@fyxer.ai', 'Hello Agent, welcome aboard!', '{datetime.utcnow()}', 'INBOUND', 0)")
        )
        
        email_id_2 = str(uuid.uuid4())
        await session.execute(
             text(f"INSERT INTO emails (id, gmail_id, thread_id, provider_message_id, subject, from_email, snippet, received_at, direction, is_read) VALUES ('{email_id_2}', 'g2', 't2', 'msg2', 'Project Update', 'client@example.com', 'Here are the specs...', '{datetime.utcnow()}', 'INBOUND', 1)")
        )
        await session.commit()
        print("Seeded 2 fake emails.")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(setup_test_data())
