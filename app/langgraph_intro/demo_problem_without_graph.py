def handle_customer_request_without_graph(user_question: str) -> str:
    """
    这是一个没有 LangGraph 的伪代码示例。

    问题：
    1. if/else 很快变复杂。
    2. 状态散落在局部变量里。
    3. 中断恢复很难。
    4. 人工确认很难插入。
    5. 每一步的输入输出不好追踪。
    """

    intent = None
    order_id = None
    order_info = None
    policy_answer = None
    need_human_confirm = False

    if "退款" in user_question:
        intent = "refund"
    elif "订单" in user_question or "物流" in user_question:
        intent = "query_order"
    else:
        intent = "general_chat"

    if intent == "general_chat":
        return "这是一个普通问题，可以走普通 Chat。"

    if intent in ["refund", "query_order"]:
        if "10001" in user_question:
            order_id = "10001"
        elif "10002" in user_question:
            order_id = "10002"
        else:
            return "请您提供订单号，我帮您继续处理。"

    if order_id == "10001":
        order_info = {
            "order_id": "10001",
            "status": "shipped",
            "status_text": "已发货",
        }
    elif order_id == "10002":
        order_info = {
            "order_id": "10002",
            "status": "paid",
            "status_text": "已付款，待发货",
        }
    else:
        return "没有查询到该订单，请检查订单号是否正确。"

    if intent == "refund":
        if order_info["status"] == "paid":
            policy_answer = "订单未发货时，可以申请取消订单并退款。"
        elif order_info["status"] == "shipped":
            policy_answer = "订单已发货后，需要收到商品后再发起退货退款申请。"
        else:
            policy_answer = "根据当前状态，建议转人工确认。"

    if need_human_confirm:
        return "该请求需要人工客服确认，我先帮您创建工单。"

    if intent == "refund":
        return (
            f"您的订单 {order_info['order_id']} 当前状态是：{order_info['status_text']}。"
            f"{policy_answer}"
        )

    return (
        f"您的订单 {order_info['order_id']} 当前状态是：{order_info['status_text']}。"
    )


def main():
    questions = [
        "我的订单 10002 还没发货，这种情况可以退款吗？",
        "帮我查一下订单 10001 到哪了？",
        "我要退款，但是忘记订单号了。",
    ]

    for question in questions:
        print("question:", question)
        print(handle_customer_request_without_graph(question))
        print("=" * 80)


if __name__ == "__main__":
    main()