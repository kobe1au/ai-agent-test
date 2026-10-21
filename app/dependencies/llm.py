from app.core.config import settings
from app.llm.base import BaseLLMProvider
from app.llm.factory import LLMProviderFactory

class MockLLMProvider:
    def __init__(self,model:str):
        self.model = model

    async def chat(self,message:str) -> str:
        return f"[{self.model}] 模拟回答：{message}"

async def get_llm_provider() -> BaseLLMProvider:
    return LLMProviderFactory.create()