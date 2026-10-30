from typing import Literal, TypedDict

from langgraph.graph import END, START, StateGraph


class BasicRouteState(TypedDict):
    user_question: str
    answer_type: str
    final_answer: str


def classify_node(state: BasicRouteState) -> dict:
    if "代码" in state["user_question"]:
        return {"answer_type": "code"}

    return {"answer_type": "text"}


def route_answer_type(
    state: BasicRouteState,
) -> Literal["text", "code"]:
    return state["answer_type"]  # type: ignore[return-value]


def text_answer_node(state: BasicRouteState) -> dict:
    return {
        "final_answer": "这是文字解释回答。"
    }


def code_answer_node(state: BasicRouteState) -> dict:
    return {
        "final_answer": "这是代码示例回答。"
    }


def build_graph():
    graph = StateGraph(BasicRouteState)

    graph.add_node("classify", classify_node)
    graph.add_node("text_answer", text_answer_node)
    graph.add_node("code_answer", code_answer_node)

    graph.add_edge(START, "classify")

    graph.add_conditional_edges(
        "classify",
        route_answer_type,
        {
            "text": "text_answer",
            "code": "code_answer",
        },
    )

    graph.add_edge("text_answer", END)
    graph.add_edge("code_answer", END)

    return graph.compile()


def main():
    app = build_graph()

    questions = [
        "解释一下 LangGraph。",
        "给我一段 LangGraph 代码。",
    ]

    for question in questions:
        result = app.invoke({
            "user_question": question,
            "answer_type": "",
            "final_answer": "",
        })

        print("question:", question)
        print("answer_type:", result["answer_type"])
        print("final_answer:", result["final_answer"])
        print("=" * 80)


if __name__ == "__main__":
    main()