from fastapi import APIRouter,Depends
from pydantic import BaseModel, Field

from app.dependencies.auth import get_current_user
from app.langchain_agents.schemas import AgentRunResponse
from app.langchain_agents.service import langchain_agent_service
from app.schemas.response import ApiResponse
from app.schemas.user import CurrentUser

router = APIRouter()

class LangchainAgentChatRequest(BaseModel):
    model: str = Field(default="deepseek-chat")
    provider: str = Field(default="deepseek")
    question: str = Field(..., description="用户问题")

@router.post("/langchain/agents/ecommerce/chat",response_model=ApiResponse[AgentRunResponse])
async def ecommerce_agent_chat(
    request: LangchainAgentChatRequest,
    current_user: CurrentUser = Depends(get_current_user),
) -> ApiResponse[AgentRunResponse]:
    return ApiResponse[AgentRunResponse](
        data=await langchain_agent_service.run_ecommerce_agent(
            user_question=request.question,
            model_name=request.model,
            provider=request.provider
        )
    )
