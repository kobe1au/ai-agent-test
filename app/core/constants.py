from enum import Enum

class AppEnv(str, Enum):
    DEVLOPMENT = "development"
    PRODUCTION = "production"
    TESTING = "testing"
    STAGING = "staging"

class ApiTag:
    HEALTH = "Health"
    CHAT = "Chat"
    CONVERSATIONS = "Conversations"
    RAG = "RAG"
    MODELS = "Models"
    AGENTS = "Agents"
    PROMPTS = "Prompts"
    STRUCTURED_OUTPUTS = "Structured Outputs"
    TOOL_CALLING = "Tool Calling"
    STRUCTURED_OUTPUTS = "LangChain Structured Outputs"
    LANGCHAIN_TOOLS = "LangChain Tools"
    LANGCHAIN_AGENTS = "LangChain Agents"
    LANGCHAIN_RAG = "LangChain RAG"
    LANGCHAIN_AGENT_RAG = "LangChain Agent RAG"
    LANGGRAPH_PERSISTENCE = "LangGraph Persistence"