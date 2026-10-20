import asyncio
from sqlalchemy import text

from app.db.session import AsyncSessionLocal   

async def main():
    async with AsyncSessionLocal() as session:
        result = await session.execute(text("select version()"))
        version = result.scalar_one()

        print(f"Database version: {version}")

if __name__ == "__main__":
    asyncio.run(main())