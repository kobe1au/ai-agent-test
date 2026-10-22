from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.redis.client import close_redis
from app.api.v1.api import api_router
from app.core.config import settings
from app.core.logging import setup_logging
from app.core.middleware import register_middleware
from app.core.exception_handlers import register_exception_handlers
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await close_redis()

def create_app() -> FastAPI:

    setup_logging()

    app = FastAPI(
        title=settings.app_name,
        description="python+FastAPI+LLM+Agent 开发实战",
        version=settings.app_version,
        debug=settings.debug,
        # lifespan 写在这里
        lifespan=lifespan,
    )
    register_middleware(app)
    register_exception_handlers(app)

    app.include_router(api_router, prefix=settings.api_v1_prefix)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "null",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/")
    async def root():
        return {
            "message": settings.app_name,
            "version": settings.app_version,
            "env": settings.app_env
        }

    return app

app = create_app()