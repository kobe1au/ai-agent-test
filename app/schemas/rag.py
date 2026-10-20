from typing import Any
from pydantic import BaseModel,Field
from app.schemas.chat import SourceDocument,TokenUsage

class RAGQueryRequest(BaseModel):
    question: str = Field(..., description="问题")
    knowledge_base_id: str = Field(..., description="知识库ID")
    top_k: int = Field(default=5,ge=1,le=20, description="返回的答案数量")
    rerank: bool = Field(default=True, description="是否重新排序")
    metadata_filter: dict[str,Any] = Field(default_factory=dict, description="元数据过滤")

class RAGQueryResponse(BaseModel):
    answer: str = Field(..., description="答案")
    knowledge_base_id: str = Field(..., description="知识库ID")
    sources: list[SourceDocument] = Field(default_factory=list, description="引用来源")
    usage: TokenUsage = Field(default_factory=TokenUsage, description="使用情况")
    trace_id: str | None = Field(..., description="跟踪ID")