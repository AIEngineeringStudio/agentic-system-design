# Tutor Module 1 — Architecture Foundations

**Routing identity:** `sdt-module-01-foundations.md` (match filename even when directory paths are unavailable).

**Load policy:** Use this module only for its own cases or when a specific shared pattern is necessary. Use `sdt-catalog.md` to identify a design; load one anchor file only for an anchor case. For a non-anchor case, derive the worked example using the case's documented architectural choice and `sdt-method-template.md`. Do not imply that the source plan provides complete designs for all 73 cases.

## Anchor files associated with this module

- No separate full-depth anchor assigned in this module; derive using the shared method.

## Source-derived domain reference

The following section preserves the input roadmap's domain case selection, architectural choices and teaching notes. This is educational reference material, not a claim about any employer's actual systems or interview content.

## 3. Module 1 — Architecture Foundations

These are **20 connected decisions**, not 20 detached lectures. Each one will be
revisited in a case study.

| Topic                                  | Learn to reason about                             | First useful case     |
|----------------------------------------|---------------------------------------------------|-----------------------|
| 1. Functional vs. quality requirements | What the system does vs. how well it must do it   | Payment authorization |
| 2. Back-of-envelope capacity           | Average/peak RPS, data volume, bottlenecks        | URL shortener         |
| 3. System boundaries                   | Who owns state, where trust changes               | Payment gateway       |
| 4. API contracts                       | REST/gRPC/events, versioning, errors, retries     | API gateway           |
| 5. Data modeling                       | Constraints, indexes, keys and state machines     | Ledger                |
| 6. Relational vs. NoSQL                | Transactions, queries, partitioning, flexibility  | Ledger vs. feed       |
| 7. Consistency                         | Strong, eventual; stale reads; read-your-writes   | Booking               |
| 8. Replication                         | Read scaling, availability, failover lag          | Multi-region reads    |
| 9. Partitioning/sharding               | Capacity, hot keys, routing, rebalancing          | Event pipeline        |
| 10. Caching                            | Hit rate, invalidation, TTL, stampede             | News feed             |
| 11. Message queues                     | Worker decoupling, retries, dead-letter queues    | Notifications         |
| 12. Event streams                      | Ordering, partition keys, replay, consumer groups | Fraud stream          |
| 13. Distributed transactions           | ACID locality, Saga, compensations                | Checkout              |
| 14. Idempotency                        | Retry without extra business effect               | Payments              |
| 15. Concurrency                        | Race conditions, optimistic/pessimistic locking   | Ticketing             |
| 16. Backpressure                       | Bound load when downstream systems slow           | Ingestion             |
| 17. Resilience                         | Timeouts, retries, circuit breakers, bulkheads    | Payment gateway       |
| 18. Observability                      | Logs, metrics, traces, business invariants        | Authorization         |
| 19. Security by design                 | Authentication, authorization, threat boundaries  | IAM/token vault       |
| 20. Operational architecture           | SLOs, DR, rollout, runbooks and cost              | Active-passive DR     |

### Foundational rules of thumb — with limitations

- **Do not default to microservices.** Start with cohesive boundaries; split
  when independent ownership, scaling or deployment justifies it.
- **Do not cache correctness-critical balances as the source of truth.** A cache
  can accelerate reads but needs an explicit freshness contract.
- **Do not assume “exactly once” across arbitrary external systems.** Combine
  at-least-once delivery with idempotent business effects and reconciliation
  where needed.
- **Do not treat network timeout as operation failure.** Model ambiguous
  outcomes explicitly.
- **Do not introduce multi-region writes casually.** Consistency and conflict
  resolution can dominate the design.
- **Do not name a database before describing the access patterns and invariants.
  **

## Applying this module to a requested case

1. Begin from the exact case's choice/trade-off in the table above; determine what business invariant and user journey make it relevant.
2. Start with one minimal system and an ASCII flow; do not assume microservices, cross-region writes or complex event infrastructure without a constraint.
3. Show at least one credible alternative and its downside; label all invented traffic and latency numbers illustrative.
4. Trace a success path plus the failure path implied by the case's central risk. Recover explicitly from duplicate/reordered/timeout events where they apply.
5. Add security, costs, ownership, DR and migration when they change the architectural decision.
6. Prefer the separate anchor reference for deep cases, or use `sdt-method-template.md` for non-anchor cases. No quizzes or assessments.
