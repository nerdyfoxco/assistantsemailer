
import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///./spine.db" 
engine = create_async_engine(DATABASE_URL, echo=False)

async def inspect():
    async with engine.connect() as conn:
        print("\n--- Indices on emails ---")
        result = await conn.execute(text("PRAGMA index_list('emails')"))
        indices = result.fetchall()
        for idx in indices:
            print(idx)
            # idx[1] is name
            name = idx[1]
            info = await conn.execute(text(f"PRAGMA index_info('{name}')"))
            print(f"  Columns: {info.fetchall()}")

        print("\n--- Table Info emails ---")
        result = await conn.execute(text("PRAGMA table_info('emails')"))
        for col in result.fetchall():
            print(col)

if __name__ == "__main__":
    asyncio.run(inspect())
