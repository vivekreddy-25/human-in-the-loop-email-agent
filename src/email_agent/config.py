"""
This is Central configuration for the email approval agent.
"""

import os
from pathlib import Path

# --- Paths ---
BASE_DIR = Path(__file__).resolve().parent.parent.parent
KNOWLEDGE_BASE_DIR = BASE_DIR / "data" / "knowledge_base"
VECTOR_STORE_PATH = BASE_DIR / "data" / "qdrant_local"

# --- Ollama models ---
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
LLM_MODEL = os.getenv("LLM_MODEL", "llama3.1:8b")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "mxbai-embed-large")

# --- Qdrant ---
QDRANT_COLLECTION_NAME = "email_agent_kb"
EMBEDDING_DIM = 1024  # mxbai-embed-large output dimension
RETRIEVAL_SCORE_THRESHOLD = float(os.getenv("RETRIEVAL_SCORE_THRESHOLD", "0.5"))

# --- Email sending ---
# Keep True until you've configured real SMTP credentials and are ready to test live sending.
DRY_RUN = os.getenv("EMAIL_DRY_RUN", "true").lower() == "true"

SMTP_HOST = os.getenv("SMTP_HOST", "")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")