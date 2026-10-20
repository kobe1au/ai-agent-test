# 模拟Agent并发调用多个tool
import asyncio
import time
from typing import Any
from pydantic import BaseModel,ValidationError,Field

class AgentRequest(BaseModel):
    user_id: str = Field(..., description="用户ID")
    order_id: str = Field(..., description="订单ID")
    question: str = Field(..., description="问题")

async def query_user(user_id: str) -> dict[str,any]:
    print("开始查询用户信息")
    asyncio.sleep(1)
    print("结束查询用户信息")
    return {"user_id": user_id, "name": "张三","age": 18}

async def query_order(order_id: str) -> dict[str,any]:
    print("开始查询订单信息")
    asyncio.sleep(1)
    print("结束查询订单信息")
    return {"order_id": order_id, "status": "待处理"} 

async def query_logistics(order_id: str) -> dict[str,any]:
    print("开始查询物流信息")
    asyncio.sleep(1)
    print("结束查询物流信息")
    return {"order_id": order_id, "status": "待处理","company": "顺丰","eta":"1天"}

async def call_llm(
        question: str,
        user_id: dict[str,any],
        order_id: dict[str,any],
        logistics_info: dict[str,any],
) -> str:
    print("开始调用LLM模型")
    asyncio.sleep(1)
    print("结束调用LLM模型")
    return "答案"

