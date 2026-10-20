from datetime import datetime
from enum import Enum
from pydantic import BaseModel,Field,field_validator
from app.schemas.chat import ChatMessage,SourceDocument,TokenUsage

class ConversationStatus(str,Enum):
    ACTIVE = "active"
    CLOSED = "closed"
    DELETED = "deleted"
    ARCHIVED = "archived"

class ConversationCreateRequest(BaseModel):
    title: str = Field(..., min_length=1,max_length=100,description="会话标题")

class ConversationResponse(BaseModel):
    conversation_id: str = Field(..., description="会话ID")
    title: str = Field(..., description="会话标题")
    status: ConversationStatus = Field(default=ConversationStatus.ACTIVE, description="会话状态")
    created_at: datetime = Field(default_factory=datetime.now, description="会话创建时间")
    updated_at: datetime = Field(default_factory=datetime.now, description="会话更新时间")

class ConversationMessagesResponse(BaseModel):
    conversation_id: str = Field(..., description="会话ID")
    messages: list[ChatMessage] = Field(default_factory=list, description="会话消息")