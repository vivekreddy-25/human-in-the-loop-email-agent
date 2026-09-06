# Human-in-the-Loop Email Agent (RAG)

An AI agent that drafts emails grounded in a local knowledge base, then pauses for human approval before sending — built with LangGraph, a local LLM (Ollama), and a local vector store (Qdrant).

## Why this exists

Autonomous agents that take real-world actions (sending emails, running queries, calling APIs) are risky without a human checkpoint. This project demonstrates a production-style pattern for pairing LLM autonomy with human oversight: the agent retrieves relevant context and drafts an email, but a human must approve, edit, or reject it before anything is actually sent.

## Architecture

Recipient + instruction
|
v
[retrieve_and_draft] --(Qdrant retrieval + Ollama LLM)--> draft email
|
v
[review] --(interrupt: waits for human)--> approve / edit / reject
|
+----+----+
| |
v v
[send] [cancel]

- **Orchestration:** LangGraph (`interrupt()` / `Command(resume=...)` pattern)
- **LLM:** Ollama, `llama3.1:8b` (fully local, no API key needed)
- **Embeddings:** Ollama, `mxbai-embed-large`
- **Vector store:** Qdrant, embedded/local mode (no server required)
- **Email sending:** SMTP, dry-run by default

## Setup

```bash
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
ollama pull llama3.1:8b
ollama pull mxbai-embed-large
```

## Usage

```bash
python main.py
```

You'll be asked for a recipient and an instruction (e.g. "follow up on invoice #123"). The agent retrieves relevant context from `data/knowledge_base/`, drafts a subject and body, then pauses for you to approve, edit, or reject before it "sends" (dry-run by default — prints instead of emailing, until SMTP credentials are configured).

## Project structure

src/email_agent/
├── config.py # paths, model names, dry-run flag
├── embeddings.py # Ollama embedding calls
├── vector_store.py # Qdrant setup + indexing
├── retriever.py # semantic search over the knowledge base
├── llm.py # Ollama chat calls for drafting
├── email_sender.py # dry-run / real SMTP sending
├── graph.py # LangGraph state machine
└── cli.py # terminal interface


## Design notes

- **Retrieval tuning:** `top_k=1` and a similarity score threshold (`RETRIEVAL_SCORE_THRESHOLD` in `config.py`) prevent irrelevant context from leaking into drafts — an early version without this threshold would inject invoice details into unrelated emails like customer welcomes.
- **Human-in-the-loop:** every draft pauses for explicit approve/edit/reject before any send action, using LangGraph's `interrupt()`/`Command(resume=...)` pattern.

## Status

Work in progress — see commit history for development stages.