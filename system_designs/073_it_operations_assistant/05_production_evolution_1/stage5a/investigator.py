"""Bounded evidence-first workflow + deterministic stand-in for an LLM."""
from datetime import datetime, timezone
import json
from typing import Any
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

from auth import Principal, authorized_incident
from tools import get_deployments, get_metrics


class InvalidModelOutput(Exception):
    pass


class MockAnalyst:
    """Deterministic model stub, NOT a real LLM or intelligent agent."""

    def analyze(self, evidence: list[dict[str, Any]]) -> dict[str, Any]:
        metrics = next((item for item in evidence if item["source"] == "monitoring"), None)
        change = next((item for item in evidence if item["source"] == "deployment"), None)
        observations = []
        if metrics is not None:
            observations.append({
                "text": f"p95 latency is {metrics['p95_latency_ms']} ms "
                        f"(baseline {metrics['baseline_p95_ms']} ms).",
                "evidence_ids": [metrics["evidence_id"]],
            })
        if change is not None:
            observations.append({
                "text": f"Version {change['version']} deployed at {change['deployed_at']}.",
                "evidence_ids": [change["evidence_id"]],
            })

        hypothesis = None
        if metrics is not None and change is not None:
            # A correlation is a hypothesis, never a confirmed root cause.
            hypothesis = {
                "text": "The recent deployment may be related; causation is unverified.",
                "evidence_ids": [metrics["evidence_id"], change["evidence_id"]],
            }
        return {
            "observations": observations,
            "hypothesis": hypothesis,
            "next_step": (
                "Compare request and database connection metrics before and after deployment."
                if hypothesis else "Restore missing evidence before diagnosing root cause."
            ),
        }


def validate_analysis(analysis: dict, evidence: list[dict]) -> None:
    """Reject missing/fabricated IDs; does not prove claim semantics."""
    allowed_ids = {item["evidence_id"] for item in evidence}
    if not isinstance(analysis, dict) or not isinstance(analysis.get("observations"), list):
        raise InvalidModelOutput("INVALID_STRUCTURE")
    claims = list(analysis["observations"])
    if analysis.get("hypothesis") is not None:
        claims.append(analysis["hypothesis"])
    for claim in claims:
        if (not isinstance(claim, dict) or not isinstance(claim.get("text"), str)
                or not isinstance(claim.get("evidence_ids"), list)
                or not claim["evidence_ids"]
                or not all(isinstance(eid, str) and eid in allowed_ids
                           for eid in claim["evidence_ids"])):
            raise InvalidModelOutput("INVALID_EVIDENCE_REFERENCE")
    if not isinstance(analysis.get("next_step"), str):
        raise InvalidModelOutput("INVALID_NEXT_STEP")


def request_optional_specialist(url: str, service: str,
                                evidence_ids: list[str]) -> dict:
    """Call a LOCAL HTTP mock; this is not A2A. Never send secrets."""
    parts = urlsplit(url)
    if (parts.scheme != "http" or parts.hostname not in {"127.0.0.1", "localhost"}
            or parts.path != "/diagnose" or parts.username is not None
            or parts.password is not None or parts.query or parts.fragment):
        raise ValueError("Only local http://127.0.0.1:<port>/diagnose is allowed")
    body = json.dumps({"service": service, "evidence_ids": evidence_ids}).encode()
    req = Request(url, data=body, headers={"Content-Type": "application/json"}, method="POST")
    with urlopen(req, timeout=2) as response:
        result = json.load(response)
    if (result.get("status") != "hypothesis_only"
            or not isinstance(result.get("suggestion"), str)
            or not isinstance(result.get("evidence_ids"), list)
            or not set(result["evidence_ids"]).issubset(set(evidence_ids))):
        raise ValueError("INVALID_SPECIALIST_RESULT")
    return result


def investigate(principal: Principal, incident_id: str, question: str,
                simulate_metrics_timeout: bool = False, analyst: Any = None,
                specialist_url: str | None = None) -> dict:
    """One request, max two primary tool reads and one analysis call."""
    if not question or len(question) > 500:
        raise ValueError("QUESTION_REQUIRED_OR_TOO_LONG")
    incident = authorized_incident(principal, incident_id)
    service, tenant = incident["service"], incident["tenant_id"]
    events: list[dict[str, str]] = []
    evidence: list[dict] = []
    missing: list[str] = []

    def mark(step: str, status: str) -> None:
        events.append({"step": step, "status": status})

    mark("incident_access", "allowed")
    try:
        evidence.append(get_metrics(principal, service, tenant, simulate_metrics_timeout))
        mark("get_metrics", "ok")
    except (TimeoutError, LookupError):
        missing.append("metrics")
        mark("get_metrics", "unavailable")

    try:
        changes = get_deployments(principal, service, tenant)
        if changes:
            evidence.extend(changes)
            mark("get_deployments", "ok")
        else:
            missing.append("deployments")
            mark("get_deployments", "unavailable")
    except LookupError:
        missing.append("deployments")
        mark("get_deployments", "unavailable")

    model = analyst if analyst is not None else MockAnalyst()
    try:
        analysis = model.analyze(evidence)
        validate_analysis(analysis, evidence)
        mark("analyze_and_validate", "ok")
    except InvalidModelOutput:
        mark("analyze_and_validate", "rejected")
        raise

    specialist = None
    warnings = []
    if specialist_url:
        try:
            specialist = request_optional_specialist(
                specialist_url, service, [item["evidence_id"] for item in evidence])
            mark("optional_specialist_http", "ok")
        except (OSError, ValueError, TimeoutError, json.JSONDecodeError) as exc:
            warnings.append("Optional specialist unavailable or returned invalid data")
            mark("optional_specialist_http", "unavailable")

    return {
        "run_id": f"RUN-{incident_id}",
        "incident_id": incident_id,
        "service": service,
        "status": "insufficient_evidence" if missing else "needs_review",
        "analysis_mode": "deterministic_mock_not_llm",
        "observations": analysis["observations"],
        "hypothesis": analysis["hypothesis"] if not missing else None,
        "next_step": ("Restore missing evidence before diagnosing root cause."
                      if missing else analysis["next_step"]),
        "evidence_ids": [item["evidence_id"] for item in evidence],
        "missing_evidence": missing,
        "specialist_suggestion": specialist,
        "warnings": warnings,
        "events": events,
        "action_executed": False,
    }
