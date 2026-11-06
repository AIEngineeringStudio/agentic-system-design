# Anchor 07 — E-commerce checkout

**Catalog case:** 28 — E-commerce checkout. **Primary module:** `sdt-module-03-scalable-apps.md`. **Optional shared concept:** `sdt-concept-02-messaging-workflows.md`. This is an **illustrative worked reference**: requirements, contracts and vendor details must be adapted to the user scenario.

## 1. Problem and scope

Coordinate checkout, stock reservation, payment and order confirmation despite independent services and irreversible side effects.

## 2. Functional requirements

Create checkout; reserve inventory; authorize/capture payment as specified; confirm/cancel order; track status and compensation.

## 3. Ranked non-functional constraints

No oversell/duplicate charge, durable workflow state and recoverability above instant completion.

## 4. Workload and assumptions

Inventory expiry, payment capture timing, shipping eligibility and compensation policy are product-specific.

## 5. Contracts and error semantics

POST /checkouts idempotent; GET /checkouts/{id}; domain events for reservation/payment/order results.

## 6. State model and invariant

Checkout(id,status,version); reservation with TTL; payment operation with provider_ref; workflow step history and recovery queue.

## 7. Minimum viable architecture (ASCII)

```text
Client -> Checkout API -> Durable workflow/orchestrator
                           |       |       |
                       Inventory Payment Order service
                           \_______outbox/events______/ 
```

## 8. Requirements -> decisions -> trade-offs

1. Use a Saga/workflow because inventory and external payment cannot share one ACID transaction.
2. Reserve stock before confirming; release reservation as a compensating action if payment fails.
3. Payment authorization and capture are distinct; choose capture timing to reduce bad recovery paths.

## 9. Critical execution paths

**Successful flow:** Create checkout -> reserve stock -> authorize payment -> create/confirm order -> capture when policy permits -> finalize and emit event.

**Failure / retry / recovery:** Reservation expires during payment; payment completes but response is lost; order write fails after payment. Track UNKNOWN and use provider reconciliation, safe compensations and operator escalation.

## 10. Scale, security and enterprise review

**Scale and reliability:** Partition workflows by checkout ID; protect hot inventory rows; bound retries with jitter; monitor stuck Saga age and compensation failure.

**Enterprise and operational readiness:** Define cross-team ownership, customer notification, cancellation/refund policy, audit traces and rollback during service version changes.

## 11. Final architecture and limitations

Start from the above baseline. Add specialized gateways, caches, partitions, secondary indexes, extra regions or queues only when a named requirement makes them necessary. Confirm state authority, trust boundaries, ambiguous outcomes, and operations before presenting a more elaborate ASCII diagram. This anchor is a **thinking framework**, not a fixed platform blueprint.

## How the design changes under a different constraint

For a single transactional store, a simpler atomic checkout may work; do not add a Saga solely for fashion.

**Tutor follow-through:** Explain each architectural choice with one alternative and a trigger for revisiting it. Do not quiz the learner or invent product-specific numbers. For the complete teaching sequence, use `sdt-method-template.md`.
