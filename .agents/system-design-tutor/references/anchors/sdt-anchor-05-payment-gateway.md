# Anchor 05 — Payment gateway

**Catalog case:** 2 — Merchant payment gateway. **Primary module:** `sdt-module-02-payments.md`. **Optional shared concept:** `sdt-concept-04-security-operations.md`. This is an **illustrative worked reference**: requirements, contracts and vendor details must be adapted to the user scenario.

## 1. Problem and scope

Expose a consistent merchant payments API while insulating callers from processor-specific protocols and failures.

## 2. Functional requirements

Authenticate merchants; validate/idempotently accept operations; route to partner adapters; normalize responses; report status and webhooks.

## 3. Ranked non-functional constraints

Secure merchant boundary, partner-specific correctness and observability, then latency and availability.

## 4. Workload and assumptions

Provider retryability, settlement support, webhook guarantees and approval semantics depend on contracts.

## 5. Contracts and error semantics

Versioned merchant-facing payment APIs, partner-specific adapters, merchant-scoped idempotency, signed webhook event format.

## 6. State model and invariant

Merchant credentials and routing policy; payment-operation records; provider references; webhook deliveries; adapter mapping/version.

## 7. Minimum viable architecture (ASCII)

```text
Merchant -> API gateway/Auth -> Payment orchestration -> Provider adapter(s) -> PSP
                                |                   |
                             Operation DB         Circuit state
                                |
                              Outbox -> Webhook delivery
```

## 8. Requirements -> decisions -> trade-offs

1. Keep a stable public contract while isolating provider differences behind adapters.
2. A local durable operation state and idempotency layer prevents blind partner retries.
3. Circuit breakers can stop repeated failing calls, but switching providers after unknown authorization status can duplicate financial effects.

## 9. Critical execution paths

**Successful flow:** Verify merchant -> validate request/key -> choose provider according to explicit routing policy -> persist and issue call -> normalize stable outcome -> deliver event.

**Failure / retry / recovery:** Provider response lost yields UNKNOWN until status verification. Consumer webhook failures retry from durable delivery log with idempotent event identifiers.

## 10. Scale, security and enterprise review

**Scale and reliability:** Use tenant quotas, provider-specific timeout budgets, isolated connection pools and visible per-partner success/unknown metrics.

**Enterprise and operational readiness:** Partner contracting, data minimization, secret rotation, audit evidence, on-call escalation and backward-compatible API upgrades.

## 11. Final architecture and limitations

Start from the above baseline. Add specialized gateways, caches, partitions, secondary indexes, extra regions or queues only when a named requirement makes them necessary. Confirm state authority, trust boundaries, ambiguous outcomes, and operations before presenting a more elaborate ASCII diagram. This anchor is a **thinking framework**, not a fixed platform blueprint.

## How the design changes under a different constraint

Adding a new processor requires explicit semantic mapping, cutover tests and safe state migration, not just a routing flag.

**Tutor follow-through:** Explain each architectural choice with one alternative and a trigger for revisiting it. Do not quiz the learner or invent product-specific numbers. For the complete teaching sequence, use `sdt-method-template.md`.
