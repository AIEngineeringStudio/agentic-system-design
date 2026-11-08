"""Synthetic identity and incident registry. NOT real authentication."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Principal:
    user_id: str
    tenant_id: str
    allowed_services: frozenset[str]


# Trusted only inside this LOCAL simulation. CLI --user is not authentication.
MOCK_PRINCIPALS = {
    "operator-5": Principal("operator-5", "company-A", frozenset({"checkout-api"})),
    "operator-9": Principal("operator-9", "company-A", frozenset({"shipping-api"})),
    "external-1": Principal("external-1", "company-B", frozenset({"checkout-api"})),
}

# The registry, not the user or model, determines incident ownership.
INCIDENTS = {
    "INC-42": {"tenant_id": "company-A", "service": "checkout-api"},
}


def simulated_identity(user_key: str) -> Principal:
    """Look up a local identity fixture. This is NOT a login mechanism."""
    if user_key not in MOCK_PRINCIPALS:
        raise PermissionError("ACCESS_DENIED")
    return MOCK_PRINCIPALS[user_key]


def authorized_incident(principal: Principal, incident_id: str) -> dict:
    incident = INCIDENTS.get(incident_id)
    if incident is None:
        raise LookupError("INCIDENT_NOT_FOUND")
    if (incident["tenant_id"] != principal.tenant_id
            or incident["service"] not in principal.allowed_services):
        raise PermissionError("ACCESS_DENIED")
    return incident.copy()
