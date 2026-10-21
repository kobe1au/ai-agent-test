# 限流
from redis.asyncio import Redis

from app.core.config import settings
from app.redis.keys import rate_limit_key

async def check_rate_limit(
        redis: Redis, 
        user_id: str,
        api_name: str
) -> tuple[bool, int, int]:
    key = rate_limit_key(user_id, api_name)

    current = await redis.incr(key)

    if current == 1:
        await redis.expire(key, settings.RATE_LIMIT_TTL_SECONDS)

    ttl = await redis.ttl(key)

    allowed = current <= settings.RATE_LIMIT_MAX_REQUESTS
    return (allowed, current, ttl)