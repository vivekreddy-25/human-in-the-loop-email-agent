"""
This section of code Wraps Ollama's embedding model (mxbai-embed-large) for turning text into vectors.
"""

import ollama
from src.email_agent import config


def embed_text(text: str) -> list[float]:
    """Returns the embedding vector for a single piece of text."""
    response = ollama.embeddings(model=config.EMBEDDING_MODEL, prompt=text)
    return response["embedding"]


def embed_batch(texts: list[str]) -> list[list[float]]:
    """Returns embedding vectors for a list of texts."""
    return [embed_text(t) for t in texts]