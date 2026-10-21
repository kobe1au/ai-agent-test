from fastapi import APIRouter,Depends
from redis.asyncio import Redis
from app.core.config import Settings, get_settings
from app.dependencies.redis import get_redis_client

router = APIRouter()

@router.get("/health")
async def health(
    settings: Settings = Depends(get_settings)
):
    return {
        "status": "ok",
        "service": settings.app_name,
        "env": settings.app_env,
        "version": settings.app_version
    }

@router.get("/error-demo")
async def error_demo():
    return {
        "message": "error demo will be implemented in exception chapter"
    }

async def get_request_source() -> str:
    return "fastapi-dependency"

@router.get("/health/redis")
async def redis_health(
    redis: Redis = Depends(get_redis_client),
):
    pong = await redis.ping()

    return {
        "status": "ok" if pong else "error",
        "redis": pong,
    }