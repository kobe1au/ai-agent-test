from pydantic import BaseModel,Field, ConfigDict
from langchain_core.prompts import ChatPromptTemplate

from app.prompts.base import PromptScenario
from app.langchain_prompts.templates import (
    AGENT_PLANNER_PROMPT,
    ECOMMERCE_CUSTOMER_SERVICE_PROMPT,
    GENERAL_CHAT_PROMPT,
    RAG_QA_PROMPT,
)

class LangchainPromptDefinition(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    prompt_id: str = Field(..., description="模板ID")
    name: str = Field(..., description="模板名称")
    scenario: PromptScenario = Field(..., description="场景")
    version: str = Field(..., description="版本")
    description: str = Field(..., description="描述")
    prompt: ChatPromptTemplate = Field(..., description="模板")
    enabled: bool = Field(True, description="是否启用")

class LangchainPromptRegistry:
    def __init__(self):
        self._prompts: dict[str,LangchainPromptDefinition] = {}

    def register(self, definition: LangchainPromptDefinition) -> None:
        key = self._build_key(
            prompt_id=definition.prompt_id,
            version=definition.version,
        )
        self._prompts[key] = definition

    def get_by_prompt_id(
            self,
            prompt_id: str,
            version: str = "v1",
        ) -> LangchainPromptDefinition | None:
        key = self._build_key(
            prompt_id=prompt_id,
            version=version,
        )
        if key not in self._prompts:
            raise KeyError(f"Prompt 不存在：{prompt_id}@{version}")

        definition = self._prompts[key]

        if not definition.enabled:
            raise KeyError(f"Prompt 已禁用：{prompt_id}@{version}")

        return definition

    def get_by_scenario(
        self,
        scenario: PromptScenario,
        version: str = "v1",
    ) -> LangchainPromptDefinition:
        for definition in self._prompts.values():
            if definition.scenario == scenario and definition.version == version and definition.enabled:
                return definition

        raise KeyError(f"未找到场景 Prompt：{scenario}@{version}")

    def list(self) -> list[LangchainPromptDefinition]:
        return list(self._prompts.values())

    def _build_key(
        self,
        prompt_id: str,
        version: str,
    ) -> str:
        return f"{prompt_id}:{version}"

langchain_prompt_registry = LangchainPromptRegistry()
langchain_prompt_registry.register(
    LangchainPromptDefinition(
        prompt_id="general_chat",
        name="通用聊天 Prompt",
        scenario=PromptScenario.GENERAL_CHAT,
        version="v1",
        description="用于普通 AI Chat 问答。",
        prompt=GENERAL_CHAT_PROMPT,
    )
)

langchain_prompt_registry.register(
    LangchainPromptDefinition(
        prompt_id="ecommerce_customer_service",
        name="电商客服 Prompt",
        scenario=PromptScenario.ECOMMERCE_CUSTOMER_SERVICE,
        version="v1",
        description="用于跨境电商客服场景。",
        prompt=ECOMMERCE_CUSTOMER_SERVICE_PROMPT,
    )
)

langchain_prompt_registry.register(
    LangchainPromptDefinition(
        prompt_id="rag_qa",
        name="RAG 问答 Prompt",
        scenario=PromptScenario.RAG_QA,
        version="v1",
        description="用于企业知识库问答。",
        prompt=RAG_QA_PROMPT,
    )
)

langchain_prompt_registry.register(
    LangchainPromptDefinition(
        prompt_id="agent_planner",
        name="Agent 规划 Prompt",
        scenario=PromptScenario.AGENT_PLANNER,
        version="v1",
        description="用于 Agent 任务规划。",
        prompt=AGENT_PLANNER_PROMPT,
    )
)