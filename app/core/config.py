from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = Field(default="ai-agent-test")
    app_env: str = Field(default="devlopment")
    app_version: str = Field(default="0.1.0")
    api_v1_prefix: str = Field(default="/api/v1")
    debug: bool = Field(default=True)

    app_api_key: str = Field(default="dev-api-key-123")

    default_model: str = Field(default="deepseek-chat")
    database_url: str = Field(default="-")
    
    supported_models: str = Field(
        default="deepseek-chat,qwen-plus"
    )
   
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )

    @property # 缓存
    def supported_model_list(self) -> list[str]:
        return [
            model.strip()
            for model in self.supported_models.split(",")
            if model.strip()
        ]

#缓存settings对象 不需要每次重新读取
@lru_cache # 缓存 
def get_settings() -> Settings:
    return Settings()

settings = get_settings()