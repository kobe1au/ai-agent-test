from app.langchain_agents.factory import (
    build_ecommerce_agent,
    parse_agent_result
)

def main():
    agent = build_ecommerce_agent(
        provider="deepseek",
        model_name="deepseek-chat",
    )

    for chunk in agent.stream({
        "messages": [{
            "role": "user",
            "content": "帮我查一下订单 10001 到哪了？",
        }]
    },
    stream_mode=True
    ):
        print("chunk:")
        print(chunk)
        print("="*80)

if __name__ == "__main__":
    main()