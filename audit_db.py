import asyncio
import json
from spine.db.database import AsyncSessionLocal
from spine.db.models import User, EmailAccount
from sqlalchemy import select

async def audit_accounts():
    async with AsyncSessionLocal() as session:
        # Get all users
        result = await session.execute(select(User))
        users = result.scalars().all()
        print(f"Total Users: {len(users)}")
        
        for user in users:
            print(f"\nUser: {user.email} (ID: {user.id})")
            # Get linked accounts
            acc_result = await session.execute(select(EmailAccount).where(EmailAccount.user_id == user.id))
            accounts = acc_result.scalars().all()
            
            if not accounts:
                print("  - No linked email accounts.")
            
            for acc in accounts:
                token_preview = "N/A"
                if acc.oauth_token_ref:
                    try:
                        data = json.loads(acc.oauth_token_ref)
                        # Try to find an email in the token data if stored, otherwise just show scopes
                        token_preview = f"Scopes: {data.get('scope')} | Access Token: {data.get('access_token')[:10]}..."
                    except:
                        token_preview = "Invalid JSON"
                
                print(f"  - Linked Account: {acc.provider} (ID: {acc.id})")
                print(f"    - Token: {token_preview}")
                print(f"    - Created At: {acc.created_at}")

if __name__ == "__main__":
    asyncio.run(audit_accounts())
