from typing import TypedDict
from langgraph.graph import END, START,StateGraph

class HelloState(TypedDict):
    user_name: str
    greeting: str

def greeting_node(state: HelloState) -> dict:
    user_name = state["user_name"]
    return {
         "greeting": f"你好，{user_name}，欢迎进入 LangGraph 阶段。"
    }

def build_graph():
    graph = StateGraph(HelloState)
    graph.add_node(START, greeting_node)
    graph.add_node("greeting", END)
    return graph.compile()

def main():
    graph = build_graph()
    state = graph.invoke({"user_name": "小王","greeting":""})
    print(state)

if __name__ == "__main__":
    main()