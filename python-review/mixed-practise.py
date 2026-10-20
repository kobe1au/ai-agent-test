# 综合练习
import asyncio
from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str
    model: str = "gpt-3.5"
    temperature: float = 0.7

class ChatResponse(BaseModel):
    model: str
    answer: str

async def call_llm(message:str,model:str,temperature:float = 0.7) -> str:
    print