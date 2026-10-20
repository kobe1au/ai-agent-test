import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.conversation import Conversation
from app.models.message import Message
from app.schemas.chat import ChatMessage, MessageRole
from app.schemas.conversation import ConversationCreateRequest

class ConversationRepository:
    async def create(
            self,
            db: AsyncSession,
            request: ConversationCreateRequest,
            user_id: str | None = None
    ) -> Conversation:
        conversation = Conversation(
            id=f"c_{uuid.uuid4().hex[:8]}",
            title=request.title,
            user_id=user_id
        )
        db.add(conversation)
        await db.commit()
        await db.refresh(conversation)

        return conversation

    async def get_messages(
            self,
            db: AsyncSession,
            conversation_id: str
    ) -> list[Message]:
        stmt = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.asc())
        )
        result = await db.execute(stmt)
        messages = result.scalars().all()

        return [
            ChatMessage(
                role=MessageRole(Message.role),
                content=message.content
            ) 
            for message in messages
        ]

    async def add_message(
        self,
        db: AsyncSession,
        conversation_id: str,
        role: str,
        content: str,
        model: str | None = None,
        prompt_tokens: int = 0,
        completion_tokens: int = 0,
        total_tokens: int = 0,
    ) -> Message:
        message = Message(
            id=f"m_{uuid.uuid4().hex[:8]}",
            conversation_id=conversation_id,
            role=role,
            content=content,
            model=model,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
        )

        db.add(message)
        await db.commit()
        await db.refresh(message)

        return message

    async def list(
        self,
        db: AsyncSession,
        offset: int = 0,
        limit: int = 10,
    ) -> list[Conversation]:
        stmt = (
            select(Conversation)
            .order_by(Conversation.created_at.desc())
            .offset(offset)
            .limit(limit)
        )

        result = await db.execute(stmt)

        return list(result.scalars().all())

    async def get_conversation_by_id(
        self,
        db: AsyncSession,
        conversation_id: str
    ) -> Conversation | None:
        stmt = (
            select(Conversation)
            .where(Conversation.id == conversation_id)
        )

        result = await db.execute(stmt)

        return result.scalars().first()
            
        


conversation_repository = ConversationRepository()