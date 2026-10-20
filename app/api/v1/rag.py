from fastapi import APIRouter,Depends

from app.schemas.rag import RAGQueryRequest, RAGQueryResponse
from app.schemas.response import ApiResponse
from app.services.rag_service import query_rag
from app.dependencies.workspace import get_workspace_id

router = APIRouter()


@router.post("/rag/query", response_model=ApiResponse[RAGQueryResponse])
async def rag_query(
    request: RAGQueryRequest,
    workspace_id: str = Depends(get_workspace_id)
) -> ApiResponse[RAGQueryResponse]:
    result = await query_rag(request)
    result.trace_id = f"{result.trace_id}_workspace_{workspace_id}"

    return ApiResponse[RAGQueryResponse](
        data=result
    )