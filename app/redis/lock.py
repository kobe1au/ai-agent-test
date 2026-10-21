# 分布式锁
# 同一个知识库不能被同时重复向量化
# 同一个订单不能同时被多个Agent处理
import uuid

from redis.asyncio import Redis

from app.redis.keys import lock_key

async def acquire_lock(
    redis: Redis,
    resource: str,
    resource_id: str,
    ttl_seconds: int = 30
) -> str | None:
    key = lock_key(resource, resource_id)

    token = str(uuid.uuid4())

    success = await redis.set(
        key,
        token,
        ex=ttl_seconds,
        nx=True # 仅当key不存在时才设置
    )

    if success:
        return token

    return None

async def release_lock(
    redis: Redis,
    resource: str,
    resource_id: str,
    token: str
) -> bool:
    key = lock_key(resource, resource_id)

    current_token = await redis.get(key)
    if current_token != token:
        return False

    await redis.delete(key)
    return True