from app.core.config import settings
from app.llm.base import BaseLLMProvider
from app.llm.factory import LLMProviderFactory
from app.langchain_models.langchain_provider import LangChainLLMProvider

class MockLLMProvider:
    def __init__(self,model:str):
        self.model = model

    async def chat(self,message:str) -> str:
        return f"[{self.model}] 模拟回答：{message}"

async def get_llm_provider() -> BaseLLMProvider:

    if settings.default_llm_provider.startswith("langchain_"):
        provider = settings.default_llm_provider.replace("langchain_", "")

        return LangChainLLMProvider(
            provider=provider,
            model=settings.default_model,
        )

    return LLMProviderFactory.create(
        provider=settings.default_llm_provider,
    )