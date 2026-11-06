# Tutor Module 4 — Distributed Transactions and Workflows

**Routing identity:** `sdt-module-04-workflows.md` (match filename even when directory paths are unavailable).

**Load policy:** Use this module only for its own cases or when a specific shared pattern is necessary. Use `sdt-catalog.md` to identify a design; load one anchor file only for an anchor case. For a non-anchor case, derive the worked example using the case's documented architectural choice and `sdt-method-template.md`. Do not imply that the source plan provides complete designs for all 73 cases.

## Anchor files associated with this module

- **Case 30 — Ticket booking:** `sdt-anchor-08-ticket-booking.md`

## Source-derived domain reference

The following section preserves the input roadmap's domain case selection, architectural choices and teaching notes. This is educational reference material, not a claim about any employer's actual systems or interview content.

## 6. Module 4 — Distributed Transactions and Workflows

|  # | Design problem           | Main architectural choice                                      |
|---:|--------------------------|----------------------------------------------------------------|
| 29 | Inventory reservation    | Atomic stock decrement, TTL reservations, expiry races         |
| 30 | Ticket booking           | Optimistic vs. pessimistic locking; unique seat constraints    |
| 31 | Driver-to-rider matching | Geospatial index, freshness, claim ownership, concurrency      |
| 32 | Order fulfillment        | Saga orchestration vs. choreography; compensating actions      |
| 33 | Coupon redemption        | Global limits, per-user uniqueness, hot keys                   |
| 34 | Wallet balance           | Immutable ledger vs. mutable read model; concurrent spending   |
| 35 | Shipment tracking        | Event ingestion, out-of-order events, eventual consistency     |
| 36 | Durable workflow engine  | State machines, timers, retries, cancellation and recovery     |
| 37 | Transactional outbox     | Atomic data update + durable event intent; relay deduplication |
| 38 | Idempotent consumer      | At-least-once events, inbox table, replay-safe side effects    |

### Key distinction

A **database transaction** protects changes inside its transactional boundary. A
**Saga** coordinates a longer business workflow across systems; compensation is
not the same as magically rolling back completed external actions. Explain what
must be compensated, what cannot be undone, and how operators recover stuck
workflows.

## Applying this module to a requested case

1. Begin from the exact case's choice/trade-off in the table above; determine what business invariant and user journey make it relevant.
2. Start with one minimal system and an ASCII flow; do not assume microservices, cross-region writes or complex event infrastructure without a constraint.
3. Show at least one credible alternative and its downside; label all invented traffic and latency numbers illustrative.
4. Trace a success path plus the failure path implied by the case's central risk. Recover explicitly from duplicate/reordered/timeout events where they apply.
5. Add security, costs, ownership, DR and migration when they change the architectural decision.
6. Prefer the separate anchor reference for deep cases, or use `sdt-method-template.md` for non-anchor cases. No quizzes or assessments.
