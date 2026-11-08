"""Stage 5A: bounded model-proposed tool selection, application-controlled execution.

The decision provider may be a scripted mock or a real hosted model.
Both are untrusted: only the application may dispatch approved operations.
"""
from dataclasses import dataclass
from typing import Any, Protocol

from auth import Principal, authorized_incident
from investigator import InvalidModelOutput, MockAnalyst, validate_analysis
from tools import get_deployments, get_metrics


class RejectedToolRequest(Exception):
    """A model proposed a tool/argument outside the permitted contract."""


@dataclass(frozen=True)
class ToolRequest:
    name: str
    arguments: dict
    call_id: str


class DecisionProvider(Protocol):
    def propose(self, incident_id: str, service: str, question: str) -> list[ToolRequest]: ...
    def analyze(self, question: str, evidence: list[dict[str, Any]]) -> dict[str, Any]: ...


class ScriptedProvider:
    """Offline, deterministic substitute for model tool calls; NOT an LLM."""
    def __init__(self, requests: list[ToolRequest] | None = None):
        self.requests = requests if requests is not None else [
            ToolRequest("get_metrics", {}, "call-1"),
            ToolRequest("get_deployments", {}, "call-2"),
        ]

    def propose(self, incident_id: str, service: str, question: str) -> list[ToolRequest]:
        return self.requests

    def analyze(self, question: str, evidence: list[dict[str, Any]]) -> dict[str, Any]:
        return MockAnalyst().analyze(evidence)


_ALLOWED = frozenset({"get_metrics", "get_deployments"})
_MAX_CALLS = 2


def _validate_requests(requests: list[ToolRequest]) -> None:
    """Reject whole proposed batch before executing any operation."""
    if not isinstance(requests, list) or len(requests) > _MAX_CALLS:
        raise RejectedToolRequest("TOOL_BUDGET_EXCEEDED")
    used_names: set[str] = set()
    used_calls: set[str] = set()
    for req in requests:
        if (not isinstance(req, ToolRequest)
                or req.name not in _ALLOWED
                or type(req.arguments) is not dict
                or req.arguments != {}
                or not isinstance(req.call_id, str)
                or not req.call_id
                or req.name in used_names
                or req.call_id in used_calls):
            raise RejectedToolRequest("TOOL_REQUEST_REJECTED")
        used_names.add(req.name)
        used_calls.add(req.call_id)


def investigate_with_model(principal: Principal, incident_id: str, question: str,
                           provider: DecisionProvider | None = None,
                           simulate_metrics_timeout: bool = False) -> dict[str, Any]:
    """Read-only incident-scoped tool invocation with a max of two tool requests.

    Does not authenticate anyone: the caller MUST supply a verified principal.
    Stage 4's simulated_identity is ONLY a local test identity fixture.
    """
    if not isinstance(question, str) or not question.strip() or len(question) > 500:
        raise ValueError("QUESTION_REQUIRED_OR_TOO_LONG")
    incident = authorized_incident(principal, incident_id)
    service, tenant = incident["service"], incident["tenant_id"]
    decision_provider = provider or ScriptedProvider()
    events: list[dict[str, str]] = [{"step": "incident_access", "status": "allowed"}]

    # No user- or model-provided service/tenant/identity is accepted by dispatch.
    requests = decision_provider.propose(incident_id, service, question)
    _validate_requests(requests)
    events.append({"step": "tool_requests", "status": "validated"})

    evidence: list[dict] = []
    missing: list[str] = []
    for req in requests:
        try:
            if req.name == "get_metrics":
                result = get_metrics(principal, service, tenant, simulate_metrics_timeout)
                evidence.append(result)
            elif req.name == "get_deployments":
                records = get_deployments(principal, service, tenant)
                if not records:
                    raise LookupError("DEPLOYMENTS_UNAVAILABLE")
                evidence.extend(records)
            events.append({"step": req.name, "status": "ok"})
        except (TimeoutError, LookupError):
            missing.append("metrics" if req.name == "get_metrics" else "deployments")
            events.append({"step": req.name, "status": "unavailable"})

    # Required evidence missing if the model chooses to skip a needed tool.
    requested_names = {req.name for req in requests}
    if "get_metrics" not in requested_names:
        missing.append("metrics")
    if "get_deployments" not in requested_names:
        missing.append("deployments")

    # An external model may generate unsupported claims. Validate the result.
    analysis = decision_provider.analyze(question, evidence)
    try:
        validate_analysis(analysis, evidence)
        events.append({"step": "validate_analysis", "status": "ok"})
    except InvalidModelOutput:
        events.append({"step": "validate_analysis", "status": "rejected"})
        raise

    return {
        "run_id": f"RUN-{incident_id}-5A",
        "incident_id": incident_id,
        "service": service,
        "status": "insufficient_evidence" if missing else "needs_review",
        "analysis_mode": "model_proposed_tools" if not isinstance(decision_provider, ScriptedProvider)
                         else "scripted_provider_not_llm",
        "observations": analysis["observations"],
        "hypothesis": None if missing else analysis["hypothesis"],
        "next_step": "Restore missing evidence before diagnosing root cause."
                     if missing else analysis["next_step"],
        "evidence_ids": [item["evidence_id"] for item in evidence],
        "missing_evidence": missing,
        "events": events,
        "action_executed": False,
    }
