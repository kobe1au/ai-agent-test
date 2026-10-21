import asyncio

from app.redis.client import redis_client, close_redis

async def main() -> None:

    pong = await redis_client.ping()
    print(f"Redis PONG: {pong}")

    await redis_client.set("course:name", "AI Agent Course",ex=60)
    value = await redis_client.get("course:name")
    print(f"course:name: {value}")

    ttl = await redis_client.ttl("course:name")
    print(f"course:name TTL: {ttl}")

    await close_redis()

if __name__ == "__main__":
    asyncio.run(main())