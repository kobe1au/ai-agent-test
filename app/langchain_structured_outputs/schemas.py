from typing import Literal

from pydantic import BaseModel, Field

class IntentClassificationResult(BaseModel):
    intent: Literal[
        "query_order",
        "refund",
        "logistics",
        "product_question",
        "human_service",
        "other"
    ] = Field(..., description="用户意图")

    confidence: float = Field(..., ge=0, le=1, description="意图置信度")

    need_order_id: bool = Field(False, description="是否需要订单号")
    reply_strategy: Literal[
        "answer_directly",
        "ask_order_id",
        "call_tool",
        "transfer_human",
        "reject",
    ] = Field(..., description="回复策略")
    reason: str = Field(..., description="判断原因")

class RAGAnswerResult(BaseModel):
    answer: str = Field(..., description=" rag 回复结果")
    is_answered: bool = Field(..., description="是否基于知识库回答了问题")
    citations: list[str] = Field(default_factory=list, description=" 引用的document_id列表")

    missing_info: str = Field(default=None, description="如果无法回答，缺少什么信息")
    confidence: float = Field(..., ge=0, le=1, description=" rag 回复的置信度")

class AgentPlanStep(BaseModel):
    step_id: int = Field(..., description="步骤id")

    name: str = Field(..., description="步骤名称")
    action_type: Literal[
        "think",
        "tool_call",
        "respond",
        "ask_user",
        "human_confirm"
    ] = Field(..., description="步骤动作类型")

    tool_name: str | None = Field(default=None, description="需要调用的工具名称")
    argument: dict = Field(default_factory=dict, description="工具参数")
    reason: str = Field(..., description="步骤执行原因")

class AgentPlanResult(BaseModel):
    goal: str = Field(..., description="用户目标")
    need_tools: bool = Field(..., description="是否需要工具")

    need_human_confirm: bool = Field(default=False, description="是否需要人工确认")

    steps: list[AgentPlanStep] = Field(default_factory=list, description="步骤列表")
    final_response_style: Literal[
        "short",
        "detailed",
        "customer_service"
    ] = Field(..., description="最终回复样式")

class ResumeReviewResult(BaseModel):
    score: int = Field(
        ...,
        ge=0,
        le=100,
        description="简历评分",
    )

    problems: list[str] = Field(
        default_factory=list,
        description="简历存在的问题",
    )

    suggestions: list[str] = Field(
        default_factory=list,
        description="优化建议",
    )

    rewritten_summary: str = Field(
        ...,
        description="改写后的项目摘要",
    )