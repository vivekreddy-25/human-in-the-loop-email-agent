"""
This is aTerminal interface that collects input, runs the graph, handles the
human-in-the-loop approval pause, and prints the final result.
"""

from langgraph.types import Command
from src.email_agent.graph import build_graph


def run_cli():
    graph = build_graph()
    thread_id = "email-thread-1"
    config = {"configurable": {"thread_id": thread_id}}

    initial_state = {
        "recipient": input("Recipient email: ").strip(),
        "instruction": input("What should this email say? (e.g. 'follow up on invoice #123'): ").strip(),
        "subject": "",
        "body": "",
        "status": "draft",
    }

    print("\nRetrieving context and drafting with the local LLM...\n")
    result = graph.invoke(initial_state, config=config)

    while "__interrupt__" in result:
        payload = result["__interrupt__"][0].value
        print("--- Human review required ---")
        print(f"To:      {payload['recipient']}")
        print(f"Subject: {payload['subject']}")
        print(f"Body:\n{payload['body']}\n")

        choice = input("Approve (a) / Edit (e) / Reject (r)? ").strip().lower()

        if choice == "a":
            decision = {"type": "accept"}
        elif choice == "e":
            decision = {
                "type": "edit",
                "subject": input("New subject: ").strip(),
                "body": input("New body: ").strip(),
            }
        else:
            decision = {"type": "reject"}

        result = graph.invoke(Command(resume=decision), config=config)

    print(f"Final status: {result['status']}")