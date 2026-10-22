from typing import Literal
from pydantic import BaseModel,Field

class IntentClassificationOutput(BaseModel):
    intent: Literal[
        "query_order",
        "refund",
        "logistics",
        "product_question",
        "human_service",
        "other",
    ] = Field(..., description="用户意图")
    confidence: float = Field(...,ge=0,le=1, description="意图置信度")

    need_order_id: bool = Field(False, description="是否需要订单ID")
    reply_strategy: Literal[
        "answer_directly",
        "ask_order_id",
        "call_tool",
        "transfer_human",
        "reject",
    ] = Field(..., description="回复策略")

    reason: str = Field(..., description="判断原因")

class RAGStructuredAnswerOutput(BaseModel):
    answer: str = Field(..., description="答案")

    is_answered: bool = Field(False, description="是否根据知识库回答了问题")

    citations: list[str] = Field(default_factory=list, description="引用文档ID列表")
    missing_info: str | None = Field(default=None, description="如果无法回答，缺少什么信息")

    confidence: float = Field(default=0,ge=0,le=1, description="答案置信度")

class AgentPlanStep(BaseModel):
    step_id: int = Field(...,ge=1, description="步骤序号")

    name: str = Field(..., description="步骤名称")

    action_type: Literal[
        "think",
        "tool_call",
        "respond",
    ] = Field(..., description="动作类型")

    tool_name: str | None = Field(default=None, description="需要调用的工具名称")
    arguments: dict | None = Field(default_factory=dict, description="工具参数")
    reason: str = Field(..., description="执行步骤的原因")

class AgentPlanOutput(BaseModel):
    goal: str = Field(..., description="用户目标")

    need_tools: bool = Field(False, description="是否需要工具")
    steps: list[AgentPlanStep] = Field(default_factory=list,min_length=1, description="执行步骤列表")

    final_response_style: Literal[
        "short",
        "detailed",
        "customer_service",
    ] = Field(
        default="short",
        description="最终回复风格",
    )

class ResumeOptimizationOutput(BaseModel):
    problems: list[str] = Field(
        default_factory=list,
        description="简历存在的问题",
    )

    suggestions: list[str] = Field(
        default_factory=list,
        description="优化建议",
    )

    rewritten_text: str = Field(
        ...,
        description="改写后的简历内容",
    )