from fastapi import APIRouter,Depends
from pydantic import BaseModel,Field
from app.dependencies.agent_context import AgentContext,get_agent_context
from app.schemas.response import ApiResponse

router = APIRouter()

class AgentRunRequest(BaseModel):
    question: str = Field(...,description="问题")
    agent_id: str = Field(default="agent_chat",description="代理ID")

class AgentRunResponse(BaseModel):
    answer: str = Field(...,description="答案")
    trace_id: str = Field(...,description="跟踪ID")
    debug: bool = Field(default=False,description="是否开启调试模式")

@router.post("/agents/run",response_model=ApiResponse[AgentRunResponse])
async def run_agent(
    request: AgentRunRequest,
    context: AgentContext = Depends(get_agent_context),
) -> ApiResponse[AgentRunResponse]:
    answer = (
        f"用户{context.current_user.username}调用了：{request.agent_id},"
        f"输入问题：{request.question}"
    )

    return ApiResponse[AgentRunResponse](
        data=AgentRunResponse(
            answer=answer,
            trace_id=context.trace_id,
            debug=context.debug,
        )
    )