import asyncio
from spine.db.database import AsyncSessionLocal
from spine.db.models import User, EmailAccount, EmailProvider
import uuid
from spine.core.security import get_password_hash
from sqlalchemy import select

async def setup_ashim():
    async with AsyncSessionLocal() as session:
        # 1. Check if user exists
        result = await session.execute(select(User).where(User.email == "ashim.khanna.cv@gmail.com"))
        user = result.scalars().first()
        
        if not user:
            print("Creating user: ashim.khanna.cv@gmail.com")
            user = User(
                id=str(uuid.uuid4()),
                email="ashim.khanna.cv@gmail.com",
                hashed_password=get_password_hash("password123"),
                name="Ashim Khanna"
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)
        else:
            print(f"User exists: {user.email} (ID: {user.id})")
            
        # 2. Check for Linked Accounts
        acc_result = await session.execute(select(EmailAccount).where(EmailAccount.user_id == user.id))
        account = acc_result.scalars().first()
        
        if account:
            print(f"Account already linked: {account.provider}")
        else:
            print("No linked Gmail account for Ashim.")
            # Check if we can steal/move the 'tester_123' token if it looks promising?
            # Or just report status.
            
        # Audit other accounts to see if Ashim's token is hiding elsewhere
        all_accounts = await session.execute(select(EmailAccount))
        for acc in all_accounts.scalars().all():
            if acc.user_id != user.id:
                print(f"Found other linked account on User ID {acc.user_id}: {acc.provider}")

if __name__ == "__main__":
    asyncio.run(setup_ashim())
