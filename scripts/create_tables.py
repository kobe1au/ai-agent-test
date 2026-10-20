import asyncio
from app.db.init_db import init_db

async def main():
    await init_db()
    print("初始化数据库成功")

if __name__ == "__main__":
    asyncio.run(main())