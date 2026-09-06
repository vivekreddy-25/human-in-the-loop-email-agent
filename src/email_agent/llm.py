"""
This is Ollama's chat model (llama3.1:8b) for drafting emails using retrieved context.
"""

import ollama
from src.email_agent import config


DRAFT_SYSTEM_PROMPT = """You are an assistant that drafts professional emails.
Use the provided context to make the email accurate and specific.
Respond ONLY in this exact format, nothing else:

SUBJECT: <subject line>
BODY:
<email body>
"""


def draft_email(recipient: str, instruction: str, context_chunks: list[str]) -> tuple[str, str]:
    """
    Generates a (subject, body) pair using the local LLM, grounded in retrieved context.
    """
    context_block = "\n\n".join(context_chunks) if context_chunks else "No additional context found."

    user_prompt = f"""Recipient: {recipient}
Instruction: {instruction}

Relevant context:
{context_block}
"""

    response = ollama.chat(
        model=config.LLM_MODEL,
        messages=[
            {"role": "system", "content": DRAFT_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
    )

    content = response["message"]["content"]
    return _parse_subject_body(content)


def _parse_subject_body(content: str) -> tuple[str, str]:
    """Parses the LLM's SUBJECT:/BODY: formatted response."""
    subject = ""
    body = ""

    if "SUBJECT:" in content and "BODY:" in content:
        subject_part = content.split("SUBJECT:")[1].split("BODY:")[0].strip()
        body_part = content.split("BODY:")[1].strip()
        subject = subject_part
        body = body_part
    else:
        # Fallback if the model didn't follow the format exactly
        subject = "Generated Email"
        body = content.strip()

    return subject, body