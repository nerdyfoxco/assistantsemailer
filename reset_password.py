import asyncio
from spine.db.database import AsyncSessionLocal
from spine.db.models import User
from spine.core.security import get_password_hash
from sqlalchemy import select, update

async def reset_password():
    email = "ashim.khanna.cv@gmail.com"
    new_password = "Apple13123$%^"
    
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.email == email))
        user = result.scalars().first()
        
        if user:
            print(f"Found user: {user.email}")
            hashed = get_password_hash(new_password)
            await session.execute(
                update(User).where(User.email == email).values(hashed_password=hashed)
            )
            await session.commit()
            print(f"Password reset successfully for {email}")
        else:
            print(f"User {email} not found!")

if __name__ == "__main__":
    asyncio.run(reset_password())
