from app.core.config import get_settings,Settings

async def get_app_settings() -> Settings:
    return get_settings()