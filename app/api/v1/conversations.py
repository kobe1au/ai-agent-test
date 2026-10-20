from fastapi import APIRouter,Path,Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.auth import get_current_user
from app.dependencies.database import get_db_session
from app.dependencies.pagination import PaginationParams
from app.schemas.conversation import (
    ConversationCreateRequest,
    ConversationMessagesResponse,
    ConversationResponse,
)
from app.schemas.response import ApiResponse
from app.schemas.user import CurrentUser
from app.services.conversation_service import (
    create_conversation,
    get_conversation_messages,
    get_conversation_by_id
)

router = APIRouter()

@router.post(
    "/conversations",
    response_model=ApiResponse[ConversationResponse]
)
async def create_new_conversation(
    request: ConversationCreateRequest,
    current_user: CurrentUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
) -> ApiResponse[ConversationResponse]:
    result = await create_conversation(
        db=db,
        request=request,
        user_id=current_user.user_id,
    )

    return ApiResponse[ConversationResponse](
        data=result
    )

@router.get(
    "/conversations/{conversation_id}/messages",
    response_model=ApiResponse[ConversationMessagesResponse]
)
async def get_messages(
    conversation_id: str = Path(..., description="会话ID"),
    db: AsyncSession = Depends(get_db_session),
) -> ApiResponse[ConversationMessagesResponse]:
    result = await get_conversation_messages(
        db=db,
        conversation_id=conversation_id,
    )

    return ApiResponse[ConversationMessagesResponse](
        data=result
    )

@router.get(
    "/conversations",
    response_model=ApiResponse[dict]
)
async def list_conversations(
    pagination: PaginationParams = Depends(PaginationParams)
) -> ApiResponse[dict]:
    return ApiResponse[dict](
        data={
            "page": pagination.page,
            "page_size": pagination.page_size,
            "offset": pagination.offset,
            "items": []
        }
    )

@router.get(
    "/conversations/{conversation_id}",
    response_model=ApiResponse[ConversationResponse]
)
async def get_conversation_by_id(
    conversation_id: str = Path(..., description="会话ID"),
    db: AsyncSession = Depends(get_db_session),
) -> ApiResponse[ConversationResponse]:
    result = await get_conversation_by_id(
        db=db,
        conversation_id=conversation_id,
    )

    return ApiResponse[ConversationResponse](
        data=result
    )
