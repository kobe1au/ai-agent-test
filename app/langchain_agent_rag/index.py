from pathlib import Path

from app.core.logging import get_logger
from app.langchain_rag.service import langchain_rag_service
from app.langchain_rag.vector_store import CHROMA_DIR

logger = get_logger(__name__)

def ensure_rag_index() -> dict:
    """
    确保本地RAG索引存在

    1. 如果 Chroma 目录不存在，就 rebuild。
    2. 如果已经存在，就跳过。
    3. 生产环境应该使用文档版本、索引版本和任务状态判断。
    """
    if not Path(CHROMA_DIR).exists():
        logger.info("rag_index_missing_rebuild_start")
        result = langchain_rag_service.rebuild_index()
        logger.info(f"rag_index_missing_rebuild_end,result={result}")

        return {
            "rebuilt": True,
            **result
        }

    return {
        "rebuilt": False,
        "message": "rag_index_exists"
    }