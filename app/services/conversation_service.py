from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.conversation_repository import conversation_repository
from app.schemas.conversation import (
    ConversationCreateRequest,
    ConversationResponse,
    ConversationMessagesResponse
)
from app.core.exceptions import AppException, ErrorCode

async def create_conversation(
        db: AsyncSession,
        request: ConversationCreateRequest,
        user_id: str | None = None
) -> ConversationResponse:
    conversation = await conversation_repository.create(
        db=db,
        request=request,
        user_id=user_id
    )

    return ConversationResponse(
        conversation_id=conversation.id,
        title=conversation.title,
        status=conversation.status,
        created_at=conversation.created_at,
        updated_at=conversation.updated_at
    )

async def get_conversation_messages(
        db: AsyncSession,
        conversation_id: str
) -> ConversationMessagesResponse:
    messages = await conversation_repository.get_messages(
        db=db,
        conversation_id=conversation_id
    )

    return ConversationMessagesResponse(
        conversation_id=conversation_id,
        messages=messages
    )

async def get_conversation_by_id(
        db: AsyncSession,
        conversation_id: str
) -> ConversationResponse | None:
    conversation = await conversation_repository.get_conversation_by_id(
        db=db,
        conversation_id=conversation_id
    )

    if conversation is None:
        raise AppException(
            error_code=ErrorCode.CONVERSATION_NOT_FOUND,
            message="查找的会话不存在"
        )

    return ConversationResponse(
        conversation_id=conversation.id,
        title=conversation.title,
        status=conversation.status,
        created_at=conversation.created_at,
        updated_at=conversation.updated_at
    )