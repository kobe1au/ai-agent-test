from enum import Enum
from pydantic import BaseModel,Field

class PromptRole(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"

class PromptScenario(str, Enum):
    GENERAL_CHAT = "general_chat"
    ECOMMERCE_CUSTOMER_SERVICE = "ecommerce_customer_service"
    RAG_QA = "rag_qa"
    AGENT_PLANNER = "agent_planner"

class PromptMessageTemplate(BaseModel):
    role: PromptRole = Field(..., description="角色")
    template: str = Field(..., description="消息模板")

class PromptTemplate(BaseModel):
    prompt_id: str = Field(..., description="提示id")
    name: str = Field(..., description="提示名称")
    scenario: PromptScenario = Field(..., description="使用场景")
    version: str = Field(default="v1", description="版本")
    description: str = Field(..., description="描述")
    messages: list[PromptMessageTemplate] = Field(..., description="消息模板列表")
    required_variables: list[str] = Field(default_factory=list, description="所需变量")
