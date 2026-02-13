import asyncio
import json
from spine.db.database import AsyncSessionLocal
from spine.db.models import EmailAccount, User
from sqlalchemy import select

async def extract_token():
    async with AsyncSessionLocal() as session:
        # Find Ashim's account
        stmt = select(EmailAccount).join(User).where(User.email == "ashim.khanna.cv@gmail.com")
        result = await session.execute(stmt)
        account = result.scalars().first()
        
        if account and account.oauth_token_ref:
            try:
                tokens = json.loads(account.oauth_token_ref)
                if "refresh_token" in tokens:
                    print(f"REFRESH_TOKEN={tokens['refresh_token']}")
                else:
                    print("ERROR: No refresh_token in JSON")
            except Exception as e:
                print(f"ERROR parsing JSON: {e}")
        else:
            print("ERROR: Account not found or empty token")

if __name__ == "__main__":
    asyncio.run(extract_token())
