from fastapi import APIRouter,Depends

from app.api.v1.chat import router as chat_router
from app.api.v1.health import router as health_router
from app.api.v1.conversations import router as conversations_router
from app.api.v1.rag import router as rag_router
from app.api.v1.models import router as model_router
from app.api.v1.agents import router as agent_router
from app.api.v1.prompts import router as prompt_router
from app.api.v1.structured_outputs import router as structured_output_router
from app.api.v1.tool_calling import router as tool_calling_router
from app.api.v1.langchain_structured_outputs import router as structured_output_router
from app.api.v1.langchain_tools import router as tool_router
from app.api.v1.langchain_agents import router as agent_router
from app.api.v1.langchain_rag import router as langchain_rag_router
from app.api.v1.langchain_agent_rag import router as langchain_agent_rag_router
from app.core.constants import ApiTag
from app.dependencies.auth import verify_api_key

api_router = APIRouter()

api_router.include_router(
    chat_router,
    tags=[ApiTag.CHAT],
    dependencies=[Depends(verify_api_key)]
)
api_router.include_router(health_router,tags=[ApiTag.HEALTH])
api_router.include_router(conversations_router, tags=[ApiTag.CONVERSATIONS], dependencies=[Depends(verify_api_key)])
api_router.include_router(rag_router,tags=[ApiTag.RAG], dependencies=[Depends(verify_api_key)])
api_router.include_router(model_router,tags=[ApiTag.MODELS])
api_router.include_router(agent_router,tags=[ApiTag.AGENTS],dependencies=[Depends(verify_api_key)])
api_router.include_router(prompt_router,tags=[ApiTag.PROMPTS])
api_router.include_router(structured_output_router,tags=[ApiTag.STRUCTURED_OUTPUTS])
api_router.include_router(
    tool_calling_router,
    tags=[ApiTag.TOOL_CALLING],
)
api_router.include_router(
    structured_output_router,
    tags=[ApiTag.STRUCTURED_OUTPUTS],
)
api_router.include_router(
    tool_router,
    tags=[ApiTag.LANGCHAIN_TOOLS],
)
api_router.include_router(
    agent_router,
    tags=[ApiTag.LANGCHAIN_AGENTS],
)
api_router.include_router(
    langchain_rag_router,
    tags=[ApiTag.LANGCHAIN_RAG],
)
api_router.include_router(
    langchain_agent_rag_router,
    tags=[ApiTag.LANGCHAIN_AGENT_RAG],
)