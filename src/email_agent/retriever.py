"""
This retrieves given a query and fetches the most relevant chunks from the vector store.
"""

from src.email_agent import config
from src.email_agent.embeddings import embed_text
from src.email_agent.vector_store import get_client


def retrieve(query: str, top_k: int = 3) -> list[str]:
    client = get_client()
    query_vector = embed_text(query)

    results = client.query_points(
        collection_name=config.QDRANT_COLLECTION_NAME,
        query=query_vector,
        limit=top_k,
    )

    relevant_chunks = [
        point.payload["text"]
        for point in results.points
        if point.score >= config.RETRIEVAL_SCORE_THRESHOLD
    ]

    return relevant_chunks