# 数据库连接和 Session 配置
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from app.core.config import settings

# 异步数据库引擎
engine = create_async_engine(
    settings.database_url,
    echo=settings.debug, # 是否打印sql
    pool_pre_ping=True # 使用连接前会先检查连接是否可用
)

# 异步 Session 工厂
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)