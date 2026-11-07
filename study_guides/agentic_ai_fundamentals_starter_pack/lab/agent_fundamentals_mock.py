#!/usr/bin/env python3
"""Small deterministic teaching mock for the Agentic AI Fundamentals Primer.

Uses only Python's standard library and synthetic data. It is deliberately NOT
an LLM agent, production service, or MCP-compatible server.
"""
from __future__ import annotations

import argparse
import json
import re
from typing import Any

POLICIES = {
    "POL-01": {
        "status": "approved",
        "text": "Unopened items may be returned within 30 days of delivery.",
    }
}

TICKETS = {
    "T-100": {"owner": "alice", "status": "in_progress", "updated_at": "2026-11-05T16:30:00Z"},
    "T-200": {"owner": "bob", "status": "open", "updated_at": "2026-11-06T10:00:00Z"},
}


def get_ticket(ticket_id: str, *, authenticated_user: str) -> dict[str, Any]:
    """The trusted service, not the proposed tool parameters, owns identity."""
    ticket = TICKETS.get(ticket_id)
    if ticket is None:
        return {"status": "error", "error": "not_found"}
    if ticket["owner"] != authenticated_user:
        return {"status": "error", "error": "forbidden"}
    return {
        "status": "ok",
        "ticket": {
            "ticket_id": ticket_id,
            "status": ticket["status"],
            "updated_at": ticket["updated_at"],
        },
    }


def answer_policy(question: str) -> dict[str, Any]:
    query = question.lower()
    # This tiny deterministic rule is intentionally not a real retriever.
    if "return" in query and "unopened" in query:
        source = POLICIES["POL-01"]
        return {
            "status": "grounded",
            "answer": f"Example approved policy: {source['text']}",
            "source_ids": ["POL-01"],
        }
    return {
        "status": "insufficient_evidence",
        "answer": "No matching approved policy was found. Ask a support agent.",
        "source_ids": [],
    }


def respond(question: str, *, authenticated_user: str) -> dict[str, Any]:
    # Deterministic routing stands in for a future bounded model decision.
    match = re.search(r"\bT-\d+\b", question.upper())
    if match:
        ticket_id = match.group(0)
        result = get_ticket(ticket_id, authenticated_user=authenticated_user)
        if result["status"] != "ok":
            return {"route": "ticket_tool", "status": result["error"], "answer": None}
        ticket = result["ticket"]
        return {
            "route": "ticket_tool",
            "status": "grounded",
            "answer": f"Ticket {ticket_id} is {ticket['status']}.",
            "source_ids": [ticket_id],
            "updated_at": ticket["updated_at"],
        }
    return {"route": "policy_lookup", **answer_policy(question)}


def smoke_test() -> None:
    assert respond("status T-100", authenticated_user="alice")["status"] == "grounded"
    assert respond("status T-200", authenticated_user="alice") == {
        "route": "ticket_tool", "status": "forbidden", "answer": None
    }
    assert respond("status T-999", authenticated_user="alice")["status"] == "not_found"
    assert respond("Can I return an unopened item?", authenticated_user="alice")["source_ids"] == ["POL-01"]
    assert respond("What is the warranty on a damaged monitor?", authenticated_user="alice")["status"] == "insufficient_evidence"
    print("PASS: 5 smoke tests (authorized, forbidden, missing, grounded, insufficient evidence)")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--user", choices=("alice", "bob"), default="alice", help="Mock authenticated user")
    parser.add_argument("--question", default="What is the status of ticket T-100?")
    parser.add_argument("--smoke", action="store_true", help="Run software smoke tests")
    args = parser.parse_args()
    if args.smoke:
        smoke_test()
    else:
        print(json.dumps(respond(args.question, authenticated_user=args.user), indent=2))


if __name__ == "__main__":
    main()
