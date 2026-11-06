# Tutor Module 2 — Payments and Financial Systems

**Routing identity:** `sdt-module-02-payments.md` (match filename even when directory paths are unavailable).

**Load policy:** Use this module only for its own cases or when a specific shared pattern is necessary. Use `sdt-catalog.md` to identify a design; load one anchor file only for an anchor case. For a non-anchor case, derive the worked example using the case's documented architectural choice and `sdt-method-template.md`. Do not imply that the source plan provides complete designs for all 73 cases.

## Anchor files associated with this module

- **Case 1 — Card authorization:** `sdt-anchor-01-card-authorization.md`
- **Case 5 — Double-entry ledger:** `sdt-anchor-02-double-entry-ledger.md`
- **Case 3 — Settlement and reconciliation:** `sdt-anchor-03-settlement-reconciliation.md`
- **Case 10 — Fraud decisioning:** `sdt-anchor-04-fraud-decisioning.md`
- **Case 2 — Payment gateway:** `sdt-anchor-05-payment-gateway.md`

## Source-derived domain reference

The following section preserves the input roadmap's domain case selection, architectural choices and teaching notes. This is educational reference material, not a claim about any employer's actual systems or interview content.

## 4. Module 2 — Payments and Financial Systems

**Priority: highest domain depth.** Trace authorization, clearing, settlement,
dispute and audit as **distinct phases**; do not flatten them into a single
database write.

|  # | Design problem                       | Why this case matters / critical choices                                        |
|---:|--------------------------------------|---------------------------------------------------------------------------------|
|  1 | Credit-card authorization            | Low-latency synchronous decision; idempotency; uncertain responses; risk checks |
|  2 | Merchant payment gateway             | API authentication, partner integration, retry contracts, provider failures     |
|  3 | Capture, clearing and settlement     | Different financial phases; batch/event workflows; finality and reconciliation  |
|  4 | Multi-provider payment orchestration | Routing, circuit breakers, provider-specific semantics, fallback safety         |
|  5 | Double-entry financial ledger        | Debit/credit invariants; immutable entries; transactional posting; auditability |
|  6 | Refunds and reversals                | State machine, partial refunds, duplicate requests, external status             |
|  7 | Chargebacks/disputes                 | Long-running workflow, deadlines, evidence, exception queues                    |
|  8 | Peer-to-peer transfer                | Atomic ledger entries, holds, concurrency, recipient identity                   |
|  9 | Recurring billing/subscriptions      | Scheduling, retry policy, failed payments, idempotent cycles                    |
| 10 | Real-time fraud detection            | Feature freshness, scoring latency, rules + models, fail-open/closed trade-off  |
| 11 | Limits and velocity controls         | Atomic counters, sliding windows, hot accounts, correct risk decisions          |
| 12 | Merchant onboarding / KYC            | Human reviews, third-party checks, long-lived durable orchestration             |
| 13 | Reconciliation engine                | Match ledgers to external files/events; discrepancies; reprocessing             |
| 14 | Transaction notifications            | Outbox, event consumers, delivery retries, user preferences                     |
| 15 | Rewards / loyalty points             | Earn/burn events, balances, expiry, reversals and consistency                   |
| 16 | Card tokenization vault              | Sensitive data isolation, tokens, HSM/KMS, audit and access boundaries          |

### Cross-cutting payment concepts to introduce in these designs

- **Financial invariants:** e.g., a balanced ledger posting must not partially
  commit; define the invariant before choosing storage.
- **Idempotency scope:** identify the business action, request fingerprint,
  retention period and response replay rules.
- **Authorization vs. settlement:** a decision to approve an authorization is
  not the same as final movement of money.
- **Exactly-once business effect:** messaging may redeliver; deduplication and
  atomic state transitions protect the actual financial effect.
- **Unknown results:** reconcile with independent sources rather than treating
  timeouts as failure.
- **PII/cardholder-data boundaries:** classify and minimize data flows; use
  applicable PCI/security controls.
- **Fraud vs. reliability:** sometimes a failing risk service implies decline,
  sometimes controlled fallback; derive it from policy and threat model.

## Applying this module to a requested case

1. Begin from the exact case's choice/trade-off in the table above; determine what business invariant and user journey make it relevant.
2. Start with one minimal system and an ASCII flow; do not assume microservices, cross-region writes or complex event infrastructure without a constraint.
3. Show at least one credible alternative and its downside; label all invented traffic and latency numbers illustrative.
4. Trace a success path plus the failure path implied by the case's central risk. Recover explicitly from duplicate/reordered/timeout events where they apply.
5. Add security, costs, ownership, DR and migration when they change the architectural decision.
6. Prefer the separate anchor reference for deep cases, or use `sdt-method-template.md` for non-anchor cases. No quizzes or assessments.
