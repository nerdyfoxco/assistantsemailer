import asyncio
from spine.db.session import async_session_maker
from spine.repositories.user_repo import UserRepository
from spine.core.security import get_password_hash
from spine.db.models import User
import uuid

async def seed():
    async with async_session_maker() as session:
        repo = UserRepository(session)
        email = "admin@example.com"
        
        # Check if exists
        # We don't have get_by_email in repo? We implemented get_by_email in UMP-20-04?
        # Let's just try to create and ignore error, or check.
        # Actually in generic repo we might not have it.
        # Let's just create generic new one with unique email to be safe, or try-catch.
        
        try:
            user = User(
                id=str(uuid.uuid4()),
                email=email,
                hashed_password=get_password_hash("password123"),
                full_name="Admin User",
                is_active=True
            )
            session.add(user)
            await session.commit()
            print(f"User {email} created.")
        except Exception as e:
            print(f"User might exist: {e}")

if __name__ == "__main__":
    asyncio.run(seed())
