import json
from app.langchain_agent_rag.factory import (
    build_ecommerce_agent_with_rag,
    parse_agent_rag_result
)
from app.langchain_agent_rag.index import ensure_rag_index

def main():
    ensure_rag_index()

    agent = build_ecommerce_agent_with_rag(
        provider="deepseek",
        model_name="deepseek-chat",
    )

    result = agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": "订单未发货时可以退款吗？",
            }
        ]
    })

    parsed = parse_agent_rag_result(result)

    print(json.dumps(
        parsed.model_dump(),
        indent=2,
        ensure_ascii=False
    ))

if __name__ == "__main__":
    main()