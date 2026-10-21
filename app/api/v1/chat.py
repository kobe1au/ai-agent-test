from fastapi import APIRouter,Path,Query,Depends
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

from app.dependencies.database import get_db_session
from app.schemas.chat import (
    ChatRequest,
    ChatResponse
)
from app.schemas.response import ApiResponse
from app.schemas.user import CurrentUser
from app.services.chat_service import chat_with_ai
from app.dependencies.auth import get_current_user
from app.dependencies.llm import MockLLMProvider, get_llm_provider
from app.dependencies.redis import get_redis_client
from app.dependencies.rate_limit import check_rate_limit


router = APIRouter()

@router.post("/chat", response_model=ApiResponse[ChatResponse],dependencies=[Depends(check_rate_limit)])
async def chat(
    request: ChatRequest,
    current_user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
    redis: Redis = Depends(get_redis_client)
) -> ApiResponse[ChatResponse]:
    result = await chat_with_ai(request,db=db,redis=redis)
    result.trace_id = f"{result.trace_id}_user_{current_user.user_id}"

    return ApiResponse[ChatResponse](
        data=result
    )


@router.post("/conversations/{conversation_id}/chat", response_model=ApiResponse[ChatResponse],dependencies=[Depends(check_rate_limit)])
async def chat_in_conversation(
    request: ChatRequest,
    conversation_id: str = Path(..., description="会话 ID"),
    debug: bool = Query(default=False, description="是否开启调试模式"),
    db: AsyncSession = Depends(get_db_session),
    redis: Redis = Depends(get_redis_client),
) -> ApiResponse[ChatResponse]:
    result = await chat_with_ai(request,db=db,redis=redis)

    if debug:
        result.trace_id = result.trace_id or "debug_trace"

    result.session_id = conversation_id

    return ApiResponse[ChatResponse](
        data=result
    )

@router.post("/chat/di-demo", response_model=ApiResponse[ChatResponse],dependencies=[Depends(check_rate_limit)])
async def chat_di_demo(
    request: ChatRequest,
    current_user: CurrentUser = Depends(get_current_user),
    llm_provider: MockLLMProvider = Depends(get_llm_provider),
) -> ApiResponse[ChatResponse]:
    latest_message = request.messages[-1].content

    answer = await llm_provider.chat(
        message=f"用户 {current_user.username} 问：{latest_message}"
    )

    result = ChatResponse(
        answer=answer,
        model=llm_provider.model,
        session_id=request.session_id,
    )

    return ApiResponse[ChatResponse](
        data=result
    )

