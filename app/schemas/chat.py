from pydantic import BaseModel,Field,field_validator
from enum import Enum
from pydantic import ConfigDict
from typing import Any
from app.core.config import settings

class MessageRole(str, Enum): # {role: user}
    SYSTEM = "system" # 系统提示词
    USER = "user" # 用户输入
    ASSISTANT = "assistant" # AI的回复
    TOOL = "tool" # 工具调用

class ChatMessage(BaseModel):
    role: MessageRole = Field(..., description="The role of the message sender")
    content: str = Field(..., description="The content of the message")

class TokenUsage(BaseModel):
    completion_tokens: int = Field(..., description="The number of completion tokens used")
    prompt_tokens: int = Field(..., description="The number of prompt tokens used")
    total_tokens: int = Field(..., description="The total number of tokens used")

class SourceDocument(BaseModel):
    document_id: str = Field(..., description="The ID of the document")
    title: str = Field(..., description="The title of the document")
    content: str = Field(..., description="The content of the document")
    score: float = Field(..., description="The score of the document")
    metadata: dict = Field(..., description="The metadata of the document")

class ChatRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    messages: list[ChatMessage] = Field(
        ...,
        min_length=1,
        description="对话消息列表"
    )
    model: str = Field(default="deepseek-chat", description="模型名称")
    temperature: float = Field(default=0.7, ge=0, le=2, description="模型温度")
    stream: bool = Field(default=False, description="是否流式输出")
    session_id: str | None = Field(default=None, description="会话 ID")
    user_id: str | None = Field(default=None, description="用户 ID")
    metadata: dict[str, Any] = Field(default_factory=dict, description="扩展元数据")
    prompt_scenario: str | None = Field(
        default=None,
        description="Prompt 场景，如 general_chat / ecommerce_customer_service / rag_qa",
    )
    prompt_version: str | None = Field(
        default="v1",
        description="Prompt 版本",
    )

    @field_validator("model")
    @classmethod
    def validate_model(cls, value: str) -> str:
        if value not in settings.supported_model_list:
            raise ValueError(f"不支持的模型：{value}")

        return value

class ChatResponse(BaseModel):
    answer: str = Field(..., description="The answer from the chatbot")
    model: str = Field(..., description="The model used for the chatbot")

    # 前端继续追问的时候带上之前的对话上下文
    session_id: str = Field(..., description="The session ID used for the chatbot")
    # 用户消息反馈 点赞 点菜等等
    message_id: str = Field(..., description="The message ID used for the chatbot")
    # 模型调用详情
    usage: TokenUsage | None = Field(..., description="The usage of the chatbot")
    #RAG引用来源
    sources: list[SourceDocument] | None = Field(..., description="The sources of the chatbot")
    # 链路追踪id 日志追踪id
    trace_id: str | None = Field(..., description="The trace ID used for the chatbot")
