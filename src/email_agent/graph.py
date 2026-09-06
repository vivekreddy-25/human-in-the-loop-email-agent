"""
This code is the LangGraph state machine which retrieve context -> draft with LLM -> human
review (interrupt) -> send or cancel.
"""

from typing import Literal, Optional, TypedDict

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
from langgraph.types import Command, interrupt

from src.email_agent.retriever import retrieve
from src.email_agent.llm import draft_email
from src.email_agent.email_sender import send_email


class EmailState(TypedDict):
    recipient: str
    instruction: str  # what the user wants the email to say, e.g. "follow up on invoice #123"
    subject: str
    body: str
    status: Optional[Literal["draft", "approved", "rejected", "sent"]]


def retrieve_and_draft_node(state: EmailState) -> EmailState:
    """Retrieves relevant context, then asks the LLM to draft the email using it."""
    context_chunks = retrieve(state["instruction"], top_k=1)
    subject, body = draft_email(state["recipient"], state["instruction"], context_chunks)
    return {**state, "subject": subject, "body": body, "status": "draft"}


def review_node(state: EmailState) -> Command[Literal["send", "cancel"]]:
    """Pauses the graph and waits for a human decision."""
    decision = interrupt(
        {
            "action": "review_email",
            "recipient": state["recipient"],
            "subject": state["subject"],
            "body": state["body"],
        }
    )

    decision_type = decision.get("type")

    if decision_type == "accept":
        return Command(goto="send")
    elif decision_type == "edit":
        return Command(
            goto="send",
            update={
                "subject": decision.get("subject", state["subject"]),
                "body": decision.get("body", state["body"]),
            },
        )
    else:  # "reject" or unrecognized -> safe default is cancel
        return Command(goto="cancel", update={"status": "rejected"})


def send_node(state: EmailState) -> EmailState:
    send_email(state["recipient"], state["subject"], state["body"])
    return {**state, "status": "sent"}


def cancel_node(state: EmailState) -> EmailState:
    print("\n[CANCELLED] Email was not sent.\n")
    return state


def build_graph():
    builder = StateGraph(EmailState)
    builder.add_node("retrieve_and_draft", retrieve_and_draft_node)
    builder.add_node("review", review_node)
    builder.add_node("send", send_node)
    builder.add_node("cancel", cancel_node)

    builder.add_edge(START, "retrieve_and_draft")
    builder.add_edge("retrieve_and_draft", "review")
    builder.add_edge("send", END)
    builder.add_edge("cancel", END)

    checkpointer = MemorySaver()
    return builder.compile(checkpointer=checkpointer)