"""LangGraph Lab 02: interrupt/resume with a fake, non-writing action.

Install: python -m pip install -U langgraph
Run: python langgraph_lab_02_approval.py

Important: InMemorySaver is not durable across process restarts. The caller's
approval must be authenticated and authorized by a separate business service.
"""
from typing import Literal, TypedDict
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import START, END, StateGraph
from langgraph.types import Command, interrupt


class ApprovalState(TypedDict, total=False):
    incident_id: str
    proposed_action: str
    decision: Literal["approved", "rejected"]
    result: str


def prepare(state: ApprovalState) -> dict:
    return {"proposed_action": "Create a mock on-call escalation"}


def review(state: ApprovalState) -> dict:
    approved = interrupt({
        "incident_id": state["incident_id"],
        "proposed_action": state["proposed_action"],
        "question": "Approve this simulated escalation?",
    })
    return {"decision": "approved" if approved is True else "rejected"}


def route(state: ApprovalState) -> Literal["approved", "rejected"]:
    return state["decision"]


def simulate_action(state: ApprovalState) -> dict:
    # This is only a local mock. No email/API/database write is made.
    return {"result": "SIMULATED: escalation would be created"}


def cancel(state: ApprovalState) -> dict:
    return {"result": "Rejected: no escalation created"}


builder = StateGraph(ApprovalState)
builder.add_node("prepare", prepare)
builder.add_node("review", review)
builder.add_node("simulate_action", simulate_action)
builder.add_node("cancel", cancel)
builder.add_edge(START, "prepare")
builder.add_edge("prepare", "review")
builder.add_conditional_edges("review", route, {
    "approved": "simulate_action", "rejected": "cancel"
})
builder.add_edge("simulate_action", END)
builder.add_edge("cancel", END)
app = builder.compile(checkpointer=InMemorySaver())

if __name__ == "__main__":
    config = {"configurable": {"thread_id": "demo-incident-42"}}
    first = app.invoke({"incident_id": "INC-42"}, config=config)
    print("Paused:", first.get("__interrupt__"))
    final = app.invoke(Command(resume=True), config=config)
    print("Final:", final)
