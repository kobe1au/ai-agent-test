from fastapi import APIRouter,Path,Query,Depends,Request
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis
from fastapi.responses import StreamingResponse

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
from app.dependencies.rate_limit import chat_rate_limit
from app.llm.base import BaseLLMProvider
from app.dependencies.llm import get_llm_provider
from app.services.chat_stream_service import stream_chat_with_ai
from app.services.tool_calling_service import tool_calling_service


router = APIRouter()

@router.post("/chat", response_model=ApiResponse[ChatResponse],dependencies=[Depends(chat_rate_limit)])
async def chat(
    request: ChatRequest,
    current_user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
    redis: Redis = Depends(get_redis_client),
    llm_provider: BaseLLMProvider = Depends(get_llm_provider),
) -> ApiResponse[ChatResponse]:
    # 给service一个和具体的LLM提供者
    result = await chat_with_ai(request,db=db,redis=redis,llm_provider=llm_provider)
    result.trace_id = f"{result.trace_id}_user_{current_user.user_id}"

    return ApiResponse[ChatResponse](
        data=result
    )


@router.post("/conversations/{conversation_id}/chat", response_model=ApiResponse[ChatResponse],dependencies=[Depends(chat_rate_limit)])
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

@router.post("/chat/di-demo", response_model=ApiResponse[ChatResponse],dependencies=[Depends(chat_rate_limit)])
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

@router.post("/chat/stream",dependencies=[Depends(chat_rate_limit)])
async def chat_stream(
    request_body: ChatRequest,
    request: Request,
    current_user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
    redis: Redis = Depends(get_redis_client),
    llm_provider: BaseLLMProvider = Depends(get_llm_provider),
) -> StreamingResponse:
    async def event_generator():
        async for event in stream_chat_with_ai(
            request=request_body,
            llm_provider=llm_provider,
            db=db,
            redis=redis
        ):
            if await request.is_disconnected():
                break
            yield event

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        }
    )