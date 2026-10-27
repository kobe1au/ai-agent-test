import json
from app.langchain_agents.factory import (
    build_ecommerce_agent,
    parse_agent_result
)

def main():
    agent = build_ecommerce_agent(
        provider="deepseek",
        model_name="deepseek-chat",
    )

    result = agent.invoke({
        "messages": [{
            "role": "user",
            "content": "帮我查一下订单 10001 到哪了？",
        }]
    })

    parsed = parse_agent_result(result)

    print(json.dumps(
        parsed.model_dump(),
        indent=2,
        ensure_ascii=False
    ))

if __name__ == "__main__":
    main()