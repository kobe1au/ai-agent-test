# 初始化数据库表
from app.db.base import Base
from app.db.session import engine

# 必须导入models,确保metadata里能收集到表
# 这里的作用是query时能找到表
from app import models

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Base.metadata.create_all
# 根据ORM模型创建数据库表