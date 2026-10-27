from langchain_core.tools import BaseTool

from app.langchain_tools.tools import ECOMMERCE_LANGCHAIN_TOOLS

class LangchainToolRegistry:
    def __init__(self):
        self._tools: dict[str, BaseTool] = {}

    def register(self, tool: BaseTool):
        self._tools[tool.name] = tool

    def get(self, name: str) -> BaseTool:
        if name not in self._tools:
            raise ValueError(f"Tool {name} not found")

        return self._tools[name]

    def list_tools(self) -> list[BaseTool]:
        return list(self._tools.values())

    def list_names(self) -> list[str]:
        return list(self._tools.keys())

    def get_many(
            self,
            names: list[str] | None = None
    ) -> list[BaseTool]:
        if not names:
            return self.list_tools()

        return [self.get(name) for name in names]

langchain_tool_registry = LangchainToolRegistry()

for tool in ECOMMERCE_LANGCHAIN_TOOLS:
    langchain_tool_registry.register(tool)