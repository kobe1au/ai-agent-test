from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from app.dependencies.auth import get_current_user
from app.langchain_tools.registry import langchain_tool_registry
from app.langchain_tools.service import langchain_tool_calling_service
from app.schemas.response import ApiResponse
from app.schemas.user import CurrentUser

router = APIRouter()

class LangchainToolChatRequest(BaseModel):
    question: str = Field(..., min_length=1,description="用户问题")
    provider: str = Field(default="deepseek",description="LLM 服务商")
    model: str = Field(default="deepseek-chat",description="LLM 模型")

@router.get("/langchain/tools",response_model=ApiResponse[list[dict]])
async def list_langchain_tools(
    current_user: CurrentUser = Depends(get_current_user)
) -> ApiResponse[list[dict]]:
    tools = langchain_tool_registry.list_tools()
    return ApiResponse[list[dict]](
        data = [
            {
                "name": tool.name,
                "description": tool.description,
                "args": tools.args
            }
            for tool in tools
        ]
    )

@router.post(
    "/langchain/tools/chat",
    response_model=ApiResponse[dict],
)
async def langchain_tool_chat(
    request: LangchainToolChatRequest,
    current_user: CurrentUser = Depends(get_current_user),
) -> ApiResponse[dict]:
    result = await langchain_tool_calling_service.run_ecommerce_customer_service(
        user_question=request.question,
        provider=request.provider,
        model_name=request.model,
    )

    return ApiResponse[dict](
        data=result
    )
