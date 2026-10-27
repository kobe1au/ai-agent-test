from langchain_core.output_parsers import StrOutputParser

from app.langchain_models.model_factory import LangChainModelFactory
from app.langchain_prompts.templates import GENERAL_CHAT_PROMPT

def main():
    model = LangChainModelFactory.create(
        provider="deepseek",
        model="deepseek-chat",
        temperature=0.7,
    )
    output_parser = StrOutputParser()

    chain = GENERAL_CHAT_PROMPT | model | output_parser

    result = chain.invoke({
        "history": [],
        "user_question": "请用三句话解释 LangChain Prompt 的作用。",
    })
                               
    print(result)


if __name__ == "__main__":
    main()