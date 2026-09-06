"""
Sets up a local (embedded, no server needed) Qdrant collection and handles
indexing documents into it.
"""

import uuid

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

from src.email_agent import config
from src.email_agent.embeddings import embed_text


def get_client() -> QdrantClient:
    """Returns a Qdrant client backed by a local on-disk path (no server needed)."""
    return QdrantClient(path=str(config.VECTOR_STORE_PATH))


def ensure_collection(client: QdrantClient) -> None:
    """Creates the collection if it doesn't already exist."""
    existing = [c.name for c in client.get_collections().collections]
    if config.QDRANT_COLLECTION_NAME not in existing:
        client.create_collection(
            collection_name=config.QDRANT_COLLECTION_NAME,
            vectors_config=VectorParams(
                size=config.EMBEDDING_DIM, distance=Distance.COSINE
            ),
        )


def index_documents(chunks: list[str]) -> None:
    """Embeds and stores a list of text chunks into the vector store."""
    client = get_client()
    ensure_collection(client)

    points = []
    for chunk in chunks:
        vector = embed_text(chunk)
        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={"text": chunk},
            )
        )

    client.upsert(collection_name=config.QDRANT_COLLECTION_NAME, points=points)