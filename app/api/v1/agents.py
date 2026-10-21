import uuid
from fastapi import APIRouter,Depends
from pydantic import BaseModel,Field
from redis.asyncio import Redis

from app.dependencies.agent_context import AgentContext,get_agent_context
from app.schemas.response import ApiResponse
from app.redis.agent_state import set_agent_run_state,get_agent_run_state
from app.dependencies.redis import get_redis_client


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
    context: AgentContext = Depends(get_agent_context)
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

@router.post("/agents/run-async", response_model=ApiResponse[dict])
async def run_agent_async(
        request: AgentRunRequest,
        context: AgentContext = Depends(get_agent_context),
        redis: Redis = Depends(get_redis_client)
) -> ApiResponse[dict]:

    run_id = f"run_{uuid.uuid4().hex[:8]}"

    await set_agent_run_state(
        redis=redis,
        run_id=run_id,
        state={
            "run_id": run_id,
            "agent_id": request.agent_id,
            "question": request.question,
            "status": "running",
            "current_step": "planning",
            "progress": 10,
            "trace_id": context.trace_id,
        },
    )

    return ApiResponse[dict](
        data={
            "run_id": run_id,
            "status": "running",
            "trace_id": context.trace_id,
        }
    )

@router.get("/agents/runs/{run_id}", response_model=ApiResponse[dict])
async def get_agent_run(
    run_id: str,
    redis: Redis = Depends(get_redis_client),
) -> ApiResponse[dict]:
    state = await get_agent_run_state(
        redis=redis,
        run_id=run_id,
    )

    if not state:
        return ApiResponse[dict](
            code=40400,
            message="Agent Run 不存在或已过期",
            data=None,
        )

    return ApiResponse[dict](
        data=state
    )