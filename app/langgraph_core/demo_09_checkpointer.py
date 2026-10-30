from typing import Annotated, TypedDict

from langchain_core.messages import AIMessage, AnyMessage, HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END,START,StateGraph
from langgraph.graph.message import add_messages

class MemoryState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

def chat_node(state: MemoryState) -> dict:
    messages = state["messages"][-1]

    return {
        "messages": [
            AIMessage(
                content=f"我记住这一轮了：{messages.content}"
            )
        ]

    }

def build_graph():
    graph = StateGraph(MemoryState)

    graph.add_node("chat",chat_node)

    graph.add_edge(START,"chat")
    graph.add_edge("chat",END)

    checkpoint = InMemorySaver()

    return graph.compile(checkpoint)

def main():
    app = build_graph()

    config = {
        "configurable":{
            "thread_id": "thread_demo_001"
        }
    }
    first_result = app.invoke({
        "messages": [
            HumanMessage(content="LangGraph 的 add_messages 是什么？")
        ]
    },config)

    print("first run:")
    for message in first_result["messages"]:
        print(message.type, ":", message.content)

    print("=" * 80)

    second_result = app.invoke(
        {
            "messages": [
                HumanMessage(content="你还记得我刚才说什么吗？")
            ]
        },
        config=config,
    )

    print("second run:")
    for message in second_result["messages"]:
        print(message.type, ":", message.content)


if __name__ == "__main__":
    main()