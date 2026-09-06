"""
This is one-off script: reads all .txt files in data/knowledge_base/ and indexes
them into the Qdrant vector store.
"""

from src.email_agent import config
from src.email_agent.vector_store import index_documents


def load_knowledge_base() -> list[str]:
    chunks = []
    for file_path in config.KNOWLEDGE_BASE_DIR.glob("*.txt"):
        text = file_path.read_text(encoding="utf-8").strip()
        if text:
            chunks.append(text)
    return chunks


if __name__ == "__main__":
    chunks = load_knowledge_base()
    print(f"Found {len(chunks)} document(s) to index.")
    index_documents(chunks)
    print("Indexing complete.")