# Anchor 01 — Card authorization

**Catalog case:** 1 — Credit-card authorization. **Primary module:** `sdt-module-02-payments.md`. **Optional shared concept:** `sdt-concept-01-correctness.md`. This is an **illustrative worked reference**: requirements, contracts and vendor details must be adapted to the user scenario.

## 1. Problem and scope

A merchant sends a card authorization request through an API and needs a timely approve, decline, or unresolved outcome while the external processor may be slow or unreachable.

## 2. Functional requirements

Accept authorization; return status; query an existing operation; emit a committed status-change event; let support operations reconcile unknown results.

## 3. Ranked non-functional constraints

Correct one-logical-operation behavior and card-data safety precede latency; then availability, partner reliability and cost.

## 4. Workload and assumptions

Treat traffic, provider capabilities, retry windows and compliance boundary as unknown until supplied. Label any scale estimates illustrative.

## 5. Contracts and error semantics

POST /authorizations with merchant-scoped idempotency key and stable request fingerprint; GET /authorizations/{id}; explicit APPROVED / DECLINED / PENDING_UNKNOWN responses. API is illustrative.

## 6. State model and invariant

Authorizations(id, merchant, request_hash, status, provider_ref, created_at); unique(merchant,idempotency_key); monotonic legal transitions. Never infer DECLINED from a timeout.

## 7. Minimum viable architecture (ASCII)

```text
Merchant -> API/Auth -> Authorization service -> Processor adapter -> External processor
                       |                 |
                       +----> transactional DB + outbox -> downstream consumers
```

## 8. Requirements -> decisions -> trade-offs

1. A transactional relational store is a simple baseline for unique idempotency keys and state transitions; an in-memory cache alone is unsafe.
2. A synchronous external call serves the immediate decision, while async notification events stay outside the critical latency path.
3. Provider timeouts become PENDING_UNKNOWN; reconcile/status-query before any safe provider retry, following actual partner semantics.

## 9. Critical execution paths

**Successful flow:** Validate identity and key -> insert pending operation -> call provider -> persist provider result and outbox -> return outcome.

**Failure / retry / recovery:** Duplicate requests return the existing logical operation; changed payload under reused key is rejected. If external processor completes but response is lost, preserve UNKNOWN and reconcile. If event dispatch fails, the outbox relay retries.

## 10. Scale, security and enterprise review

**Scale and reliability:** Rate-limit tenants, isolate slow providers, measure p95/p99 latency and unresolved states; add partitions/queues only where bottlenecks require.

**Enterprise and operational readiness:** Tokenize/minimize cardholder data, scope trusted systems, protect credentials, retain appropriate audit evidence, define external partner SLAs and incident ownership.

## 11. Final architecture and limitations

Start from the above baseline. Add specialized gateways, caches, partitions, secondary indexes, extra regions or queues only when a named requirement makes them necessary. Confirm state authority, trust boundaries, ambiguous outcomes, and operations before presenting a more elaborate ASCII diagram. This anchor is a **thinking framework**, not a fixed platform blueprint.

## How the design changes under a different constraint

If offline authorization is allowed, add explicit policy and risk limits; if multiple acquirers are used, routing and nonduplicating failover become a new design problem.

**Tutor follow-through:** Explain each architectural choice with one alternative and a trigger for revisiting it. Do not quiz the learner or invent product-specific numbers. For the complete teaching sequence, use `sdt-method-template.md`.
