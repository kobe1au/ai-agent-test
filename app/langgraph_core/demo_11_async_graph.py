import asyncio
from typing import TypedDict

from langgraph.graph import END,START,StateGraph

class AsyncState(TypedDict):
    answer: str
    user_question: str

async def async_answer_node(state: AsyncState) -> dict:
    await asyncio.sleep(1)

    return {
        "answer": f"异步节点已经处理完成：{state['user_question']}"
    }

def build_graph():
    graph = StateGraph(AsyncState)

    graph.add_node("answer",async_answer_node)

    graph.add_edge(START, "answer")
    graph.add_edge("answer", END)

    return graph.compile()

async def main():
    app = build_graph()

    result = await app.ainvoke({
        "user_question": "LangGraph 支持异步节点吗？",
        "answer": "",
    })

    print(result)

    print("=" * 80)
    print("astream updates:")

    async for chunk in app.astream(
        {
            "user_question": "再测试一下异步 stream。",
            "answer": "",
        },
        stream_mode="updates",
    ):
        print(chunk)


if __name__ == "__main__":
    asyncio.run(main())