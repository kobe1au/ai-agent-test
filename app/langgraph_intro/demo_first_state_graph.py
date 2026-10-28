from typing import TypedDict

from langgraph.graph import END,START,StateGraph

class SimpleState(TypedDict):
    user_question: str
    answer: str

def answer_node(State: SimpleState) -> dict:
    question = State["user_question"]
    return {
        "answer": f"你问的是：{question}。这是 LangGraph 的第一个节点回答。"
    }

def build_graph():
    graph = StateGraph()
    graph.add_node("answer_node", answer_node)
    graph.add_edge(START, "answer_node")
    graph.add_edge("answer_node", END)

    return graph.compile()

def main():
    app = build_graph()

    result = app.invoke({
        "user_question": "你叫什么名字？",
        "answer": "",
    })
    print(result.model_dump())

if __name__ == "__main__":
    main()