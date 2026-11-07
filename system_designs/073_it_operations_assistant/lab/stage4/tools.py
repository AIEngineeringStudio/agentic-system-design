"""Two approved read-only tools over synthetic source-of-truth fixtures."""
import json
from pathlib import Path
from typing import TypedDict
from auth import Principal

DATA_DIR = Path(__file__).resolve().parent / "data"


class MetricsEvidence(TypedDict):
    evidence_id: str
    source: str
    tenant_id: str
    service: str
    recorded_at: str
    p95_latency_ms: int
    baseline_p95_ms: int
    error_rate_percent: float


class DeploymentEvidence(TypedDict):
    evidence_id: str
    source: str
    tenant_id: str
    service: str
    version: str
    deployed_at: str


def _assert_can_read(principal: Principal, service: str, tenant_id: str) -> None:
    # Authorization is repeated at this data boundary, not just at the API.
    if tenant_id != principal.tenant_id or service not in principal.allowed_services:
        raise PermissionError("ACCESS_DENIED")


def _load_records(filename: str) -> list[dict]:
    return json.loads((DATA_DIR / filename).read_text(encoding="utf-8"))


def get_metrics(principal: Principal, service: str, tenant_id: str,
                simulate_timeout: bool = False) -> MetricsEvidence:
    _assert_can_read(principal, service, tenant_id)
    if simulate_timeout:
        raise TimeoutError("MONITORING_TIMEOUT")
    matches = [record for record in _load_records("metrics.json")
               if record["service"] == service and record["tenant_id"] == tenant_id]
    if len(matches) != 1:
        raise LookupError("METRICS_UNAVAILABLE")
    return matches[0]


def get_deployments(principal: Principal, service: str,
                    tenant_id: str) -> list[DeploymentEvidence]:
    _assert_can_read(principal, service, tenant_id)
    return [record for record in _load_records("deployments.json")
            if record["service"] == service and record["tenant_id"] == tenant_id]
