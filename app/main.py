from fastapi import FastAPI

from app.api.v1.api import api_router
from app.core.config import settings
from app.core.logging import setup_logging
from app.core.middleware import register_middleware
from app.core.exception_handlers import register_exception_handlers

def create_app() -> FastAPI:

    setup_logging()

    app = FastAPI(
        title=settings.app_name,
        description="python+FastAPI+LLM+Agent 开发实战",
        version=settings.app_version,
        debug=settings.debug
    )
    register_middleware(app)
    register_exception_handlers(app)

    app.include_router(api_router, prefix=settings.api_v1_prefix)

    @app.get("/")
    async def root():
        return {
            "message": settings.app_name,
            "version": settings.app_version,
            "env": settings.app_env
        }

    return app

app = create_app()