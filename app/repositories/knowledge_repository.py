from typing import Any
from app.schemas.chat import SourceDocument

class KnowledgeRepository:
    async def search_documents(
        self,
        question: str,
        knowledge_base_id: str,
        metadata_filter: dict[str,Any] = None,
        rerank: bool = True,
        top_k: int = 5
    ) -> list[SourceDocument]:
        return [
            SourceDocument(
                document_id="doc_001",
                title="企业知识库说明文档",
                content="RAG 是 Retrieval Augmented Generation，用于结合外部知识增强大模型回答。",
                score=0.89,
                metadata={
                    "knowledge_base_id": knowledge_base_id,
                    "page": 1,
                    "filter": metadata_filter or {}
                },
            )
        ][:top_k]

knowledge_repository = KnowledgeRepository()