# Anchor 08 — Ticket booking

**Catalog case:** 30 — Ticket booking. **Primary module:** `sdt-module-04-workflows.md`. **Optional shared concept:** `sdt-concept-01-correctness.md`. This is an **illustrative worked reference**: requirements, contracts and vendor details must be adapted to the user scenario.

## 1. Problem and scope

Reserve and sell a unique seat under high contention without double-selling after concurrent requests or checkout timeouts.

## 2. Functional requirements

Search seats; place time-limited hold; confirm purchase; release/expire hold; report authoritative status.

## 3. Ranked non-functional constraints

At most one confirmed owner per seat, clear hold expiration and understandable user feedback.

## 4. Workload and assumptions

Holding duration, payment rules, ticket transfer and venue capacity are explicit product constraints.

## 5. Contracts and error semantics

POST /holds {seat_id, buyer_id}; POST /holds/{id}/confirm; GET /seats/{id}.

## 6. State model and invariant

Seats(id, status, version); Holds(id, seat_id, buyer_id, expires_at, status); unique active ownership/confirmed seat enforced in transactional store.

## 7. Minimum viable architecture (ASCII)

```text
Buyers -> Booking API -> Seat/Hold transaction DB
                          |           |
                          |        Expiration worker
                          +-> Payment workflow -> Confirmation/outbox
```

## 8. Requirements -> decisions -> trade-offs

1. Optimistic conditional updates work when conflicts are modest; locks/serial allocation may be justified for flash-sale hotspots.
2. Seat hold must be authoritative in the transactional store, not only a TTL cache.
3. Confirmation and payment form a workflow with a clear ordering/recovery policy.

## 9. Critical execution paths

**Successful flow:** Atomically hold an available seat -> display deadline -> verify hold still valid -> complete payment policy -> confirm one owner.

**Failure / retry / recovery:** Two simultaneous holds: one wins. Expiry vs confirm: atomic state transition resolves race. Payment succeeds but response lost: reconcile without selling twice.

## 10. Scale, security and enterprise review

**Scale and reliability:** Partition by event/venue where possible; precompute browse views while verifying final availability in authoritative state; monitor contention and expired holds.

**Enterprise and operational readiness:** Access controls for organizers/resellers, anti-bot quotas, refund/chargeback handling, fraud audit trail and operational support.

## 11. Final architecture and limitations

Start from the above baseline. Add specialized gateways, caches, partitions, secondary indexes, extra regions or queues only when a named requirement makes them necessary. Confirm state authority, trust boundaries, ambiguous outcomes, and operations before presenting a more elaborate ASCII diagram. This anchor is a **thinking framework**, not a fixed platform blueprint.

## How the design changes under a different constraint

If seats are fungible general admission, bounded inventory counters are simpler than unique-seat state machines.

**Tutor follow-through:** Explain each architectural choice with one alternative and a trigger for revisiting it. Do not quiz the learner or invent product-specific numbers. For the complete teaching sequence, use `sdt-method-template.md`.
