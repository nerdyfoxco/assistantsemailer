
import asyncio
from spine.db.database import AsyncSessionLocal
from spine.db.models import EmailAccount, User
from sqlalchemy import select

async def check_accounts():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(EmailAccount))
        accounts = result.scalars().all()
        
        print(f"Found {len(accounts)} email accounts.")
        for acc in accounts:
            print(f"User: {acc.user_id} | Provider: {acc.provider} | Token Len: {len(acc.oauth_token_ref)}")
            if len(acc.oauth_token_ref) > 50:
                 print("-> HAS TOKEN (Candidate for Real Test)")
            else:
                 print("-> NO TOKEN (Invalid)")

if __name__ == "__main__":
    asyncio.run(check_accounts())
