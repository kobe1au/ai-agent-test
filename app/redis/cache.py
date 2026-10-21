# 缓存封装
import json
from redis.asyncio import Redis
import hashlib

from app.core.config import settings
from app.redis.keys import conversation_recent_messages_key
from app.schemas.chat import ChatMessage, MessageRole
from app.redis.keys import chat_response_cache_key,api_key_cache_key

# 缓存key
def hash_text(text:str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]

async def get_cached_chat_response(
        redis: Redis,
        question: str
) -> str | None:
    key = chat_response_cache_key(hash_text(question))
    value = await redis.get(key)
    if not value:
        return None
    return value.decode("utf-8")

async def cache_chat_response(
        redis: Redis,
        question: str,
        answer: str,
        ttl_seconds: int = 300
):
    key = chat_response_cache_key(hash_text(question))
    await redis.set(
        key,
        answer,
        ex=ttl_seconds
    )
    
async def cache_recent_messages(
        redis: Redis,
        conversation_id: str,
        messages: list[ChatMessage],
        ttl_seconds: int | None = None
):
    key = conversation_recent_messages_key(conversation_id)

    data = [
        {
            "role": message.role,
            "content": message.content,
        }
        for message in messages
    ]

    await redis.set(
        key,
        json.dumps(data),
        ttl_seconds or settings.redis_default_ttl_seconds,
    )

async def get_cached_recent_messages(
        redis: Redis,
        conversation_id: str
) -> list[ChatMessage] | None:
    key = conversation_recent_messages_key(conversation_id)
    value = await redis.get(key)

    if not value:
        return None

    data = json.loads(value)
    return [
        ChatMessage(
            role=MessageRole(message["role"]),
            content=message["content"],
        )
        for message in data
    ]

async def cache_api_key_user(
        redis: Redis,
        api_key_hash: str,
        user_id: str,
        ttl_seconds: int = 600
):
    key = api_key_cache_key(api_key_hash)
    await redis.set(
        key,
        user_id,
        ttl_seconds
    )

async def get_cached_api_key_user(
    redis: Redis,
    api_key_hash: str,
) -> str | None:
    key = api_key_cache_key(api_key_hash)

    return await redis.get(key)