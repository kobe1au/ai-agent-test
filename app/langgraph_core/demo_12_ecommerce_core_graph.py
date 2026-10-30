import operator
from typing import Annotated, Literal, TypedDict
from langgraph.graph import END,START,StateGraph

class EcommerceCoreState(TypedDict):
    user_question: str
    intent: str
    order_id: str | None
    order_status: str | None
    policy_type: str | None
    policy_answer: str | None
    final_answer: str
    logs: Annotated[list[str], operator.add]

def classify_intent_node(state: EcommerceCoreState) -> dict:
    question = state["user_question"]

    question = state["user_question"]

    if "退款" in question or "退货" in question:
        intent = "refund"
    elif "订单" in question or "物流" in question:
        intent = "order"
    else:
        intent = "general"

    return {
        "intent": intent,
        "logs": [f"classify_intent：识别意图为 {intent}"],
    }

def route_by_intent(
    state: EcommerceCoreState,
) -> Literal["general", "need_order"]:
    if state["intent"] == "general":
        return "general"

    return "need_order"

def extract_order_id_node(state: EcommerceCoreState) -> dict:
    question = state["user_question"]

    if "10001" in question:
        order_id = "10001"
    elif "10002" in question:
        order_id = "10002"
    else:
        order_id = None

    return {
        "order_id": order_id,
        "logs": [f"extract_order_id：订单号为 {order_id}"],
    }

def route_after_extract_order_id(
    state: EcommerceCoreState,
) -> Literal["ask_order_id", "query_order"]:
    if not state["order_id"]:
        return "ask_order_id"

    return "query_order"

def ask_order_id_node(state: EcommerceCoreState) -> dict:
    return {
        "final_answer": "请您提供订单号，我才能继续查询订单状态和售后规则。",
        "logs": ["ask_order_id：缺少订单号，追问用户。"],
    }

def query_order_node(state: EcommerceCoreState) -> dict:
    order_id = state["order_id"]

    if order_id == "10001":
        order_status = "shipped"
        status_text = "已发货"
    elif order_id == "10002":
        order_status = "paid"
        status_text = "已付款，待发货"
    else:
        order_status = "not_found"
        status_text = "未查询到订单"

    return {
        "order_status": order_status,
        "logs": [f"query_order：订单状态为 {status_text}"],
    }
