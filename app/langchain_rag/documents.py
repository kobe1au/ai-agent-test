from pathlib import Path
from langchain_core.documents import Document

KNOWLEDGE_BASE_DIR = Path("data/knowledge_base")

def load_markdown_documents(
        base_dir =  KNOWLEDGE_BASE_DIR,
) -> list[Document]:

    documents: list[Document] = []

    for file_path in sorted(base_dir.glob("*.md")):
        content = file_path.read_text(encoding="utf-8")

        document_id = file_path.stem
        documents.append(
            Document(
                page_content=content, 
                metadata={
                    "source": str(file_path),
                    "file_name": file_path.name,
                    "document_id": document_id,
                    "file_type": "markdown",
                }
            )
        )

    return documents

def print_documents(documents: list[Document]):
    for index, doc in enumerate(documents):
        print(f"Document {index}")
        print("metadata:", doc.metadata)
        print("content preview:", doc.page_content[:120])
        print("=" * 80)