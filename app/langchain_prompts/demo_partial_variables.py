from datetime import datetime
from langchain_core.prompts import ChatPromptTemplate

def main():
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            (
                "你是一个专业的 {role_name}。\n"
                "当前日期：{current_date}\n"
                "回答要求：{answer_style}"
            ),
        ),
        (
            "human",
            "{user_question}",
        ),
    ])

    prompt = prompt.partial(answer_style="结构清晰。")

    prompt_value = prompt.invoke({
        "user_question": "你好",
    })

    for message in prompt_value.messages:
        print(message.type,":",message.content)
        print("-"*60)

if __name__ == "__main__":
    main()