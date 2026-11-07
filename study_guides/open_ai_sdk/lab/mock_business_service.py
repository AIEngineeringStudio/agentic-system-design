from dataclasses import dataclass

@dataclass(frozen=True)
class Principal:
    user_id: str
    tenant_id: str

# Synthetic records only.
RECORDS = {
    "T-100": {"tenant_id": "A", "owner_id": "u1", "status": "open"},
    "T-200": {"tenant_id": "B", "owner_id": "u2", "status": "closed"},
}

def read_ticket(principal: Principal, ticket_id: str) -> dict:
    record = RECORDS.get(ticket_id)
    if record is None:
        return {"result": "not_available"}
    if (record["tenant_id"], record["owner_id"]) != (
        principal.tenant_id, principal.user_id
    ):
        return {"result": "not_available"}
    return {"result": "ok", "ticket_id": ticket_id,
            "status": record["status"]}
