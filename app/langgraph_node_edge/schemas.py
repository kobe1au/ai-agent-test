import operator
from typing import Annotated, Literal, TypedDict

class OrderInfo(TypedDict,total=False):
    order_id: str
    status: str
    status_text: str
    tracking_company: str | None
    tracking_no: str | None
    latest_event: str | None

class SourceInfo(TypedDict,total=False):
    chunk_id: str
    content_preview: str
    document_id: str
    score: float
    source: str

class ToolCallInfo(TypedDict,total=False):
    args: dict
    id: str
    name: str
    result_preview: str
    success: bool

class EcommerceAgentState(TypedDict,total=False):
    user_question: str

    intent: Literal[
        "general",
        "query_order",
        "logistics",
        "refund",
        "after_sales",
        "human_service",
        "unknown",
    ]

    order_id: str
    order_info: OrderInfo | None

    policy_query: str | None
    policy_answer: str | None
    sources: Annotated[list[SourceInfo],operator.add]

    need_human_confirm: bool
    risk_level: Literal["low", "medium", "high"]
    pending_action: str | None

    tool_calls: Annotated[list[ToolCallInfo],operator.add]
    logs: Annotated[list[str],operator.add]
    errors: Annotated[list[str],operator.add]

    final_answer: str
    is_finished: bool
    retry_count: int
