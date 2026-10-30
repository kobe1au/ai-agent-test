from typing import TypedDict, NotRequired
from langgraph.graph import END,START,StateGraph

class ProfileState(TypedDict):
    user_name: str
    role: NotRequired[str]
    intro: NotRequired[str]

def fill_role_node(state: ProfileState) -> dict:
    return {
        "role": "程序员"
    }

def generate_intro_node(state: ProfileState) -> dict:
    return {
        "intro": f"我是{state['user_name']}，我是一个{state['role']}"
    }

def build_graph():
    graph = StateGraph(ProfileState)
    graph.add_node("fill_role",fill_role_node)
    graph.add_node("generate_intro",generate_intro_node)

    graph.add_edge(START,"fill_role")
    graph.add_edge("fill_role","generate_intro")
    graph.add_edge("generate_intro",END)

    return graph.compile()

def main():
    graph = build_graph()
    state = ProfileState(user_name="张三")

    result = graph.invoke(state)
    print(result)

if __name__ == "__main__":
    main()   