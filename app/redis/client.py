# 创建redis客户端
from redis.asyncio import Redis

from app.core.config import settings

redis_client = Redis.from_url(
    settings.redis_url,
    decode_responses=True, # 默认是bytes，这里改为str
    encoding="utf-8"
)

async def close_redis():
    await redis_client.aclose()