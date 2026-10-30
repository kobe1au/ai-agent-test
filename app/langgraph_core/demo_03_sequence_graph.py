from typing import TypedDict, NotRequired
from langgraph.graph import END,START,StateGraph

class LessonState(TypedDict):
    topic: str
    outline: NotRequired[str]
    script: NotRequired[str]
    summary: NotRequired[str]

def generate_outline_node(state: LessonState) -> dict:
    return {
         "outline": f"《{state['topic']}》课程大纲：概念、代码、项目、总结。"
    }

def generate_script_node(state: LessonState) -> dict:
    return {
        "script": f"根据大纲生成重点内容：{state['outline']}"
    }


def generate_summary_node(state: LessonState) -> dict:
    return {
        "summary": f"本节课围绕 {state['topic']}，完成了大纲和重点内容。"
    }

def build_graph():
    graph = StateGraph(LessonState)

    graph.add_node("generate_outline", generate_outline_node)
    graph.add_node("generate_script", generate_script_node)
    graph.add_node("generate_summary", generate_summary_node)

    graph.add_edge(START, "generate_outline")
    graph.add_edge("generate_outline", "generate_script")
    graph.add_edge("generate_script", "generate_summary")
    graph.add_edge("generate_summary", END)
    return graph.compile()

def main():
    graph = build_graph()
    state = LessonState(topic="机器学习")
    result = graph.invoke(state)
    print(result)


