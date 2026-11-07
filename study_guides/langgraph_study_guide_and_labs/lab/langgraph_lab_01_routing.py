"""LangGraph Lab 01: deterministic incident routing; no LLM/API key required.

Install: python -m pip install -U langgraph
Run: python langgraph_lab_01_routing.py
"""
from typing import Literal, TypedDict
from langgraph.graph import START, END, StateGraph


class IncidentState(TypedDict, total=False):
    alert: str
    severity: Literal["low", "high"]
    evidence: list[str]
    recommendation: str


def classify(state: IncidentState) -> dict:
    text = state["alert"].lower()
    severity = "high" if any(x in text for x in ("down", "outage", "payment")) else "low"
    return {"severity": severity}


def route(state: IncidentState) -> Literal["high", "low"]:
    return state["severity"]


def investigate(state: IncidentState) -> dict:
    return {"evidence": ["mock-metrics: 5xx rate increased", "mock-logs: 504 spike"]}


def recommend(state: IncidentState) -> dict:
    return {"recommendation": "Escalate for on-call review; no action executed."}


def close_low(state: IncidentState) -> dict:
    return {"recommendation": "Record and monitor; no action executed."}


builder = StateGraph(IncidentState)
builder.add_node("classify", classify)
builder.add_node("investigate", investigate)
builder.add_node("recommend", recommend)
builder.add_node("close_low", close_low)
builder.add_edge(START, "classify")
builder.add_conditional_edges("classify", route, {"high": "investigate", "low": "close_low"})
builder.add_edge("investigate", "recommend")
builder.add_edge("recommend", END)
builder.add_edge("close_low", END)
app = builder.compile()

if __name__ == "__main__":
    for alert in ("Payments down in west region", "Disk usage 65 percent"):
        result = app.invoke({"alert": alert})
        print(result)
