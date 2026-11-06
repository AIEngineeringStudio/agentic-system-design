# Anchor 04 — Fraud decisioning

**Catalog case:** 10 — Real-time fraud detection. **Primary module:** `sdt-module-02-payments.md`. **Optional shared concept:** `sdt-concept-04-security-operations.md`. This is an **illustrative worked reference**: requirements, contracts and vendor details must be adapted to the user scenario.

## 1. Problem and scope

Score a financial activity for fraud fast enough to affect the authorization path, using rules and/or a predictive model.

## 2. Functional requirements

Accept transaction context; fetch fresh risk features; evaluate rules/model; return allow/decline/review with decision reasons; log evidence.

## 3. Ranked non-functional constraints

Bounded decision latency, policy safety, feature freshness, model governance and explainability.

## 4. Workload and assumptions

Thresholds, model accuracy, permitted fail-open/closed choices and latency budgets require explicit risk-policy input.

## 5. Contracts and error semantics

POST /risk-decisions {operation_id, context}; response {decision, reason_codes, policy_version, model_version}.

## 6. State model and invariant

Features by entity/time; rule and model versions; immutable decision evidence; feature update event log.

## 7. Minimum viable architecture (ASCII)

```text
Payment request -> Risk API -> Policy/rules + model serving
                              |
                     Online feature view <- Stream processing <- Events
                              |
                       Decision evidence store
```

## 8. Requirements -> decisions -> trade-offs

1. Use stable rules for required policy and model scoring for richer patterns where justified.
2. Separate feature-ingestion from the synchronous scoring path but state permitted staleness.
3. Choose outage fallback according to risk ownership; neither automatic allow nor automatic deny is universally correct.

## 9. Critical execution paths

**Successful flow:** Normalize transaction -> retrieve applicable features -> evaluate policy/model under budget -> persist decision evidence -> respond.

**Failure / retry / recovery:** Missing/old features use a declared fallback. On scoring timeout, preserve an explicit unavailable/controlled decision path. Deduplicate incoming events so counters do not inflate.

## 10. Scale, security and enterprise review

**Scale and reliability:** Partition features by entity key, watch hot merchants/cards, instrument freshness and tail latency, support controlled model rollout and rollback.

**Enterprise and operational readiness:** Privacy restrictions, access control, auditability, model monitoring, drift review and human case escalation are first-class requirements.

## 11. Final architecture and limitations

Start from the above baseline. Add specialized gateways, caches, partitions, secondary indexes, extra regions or queues only when a named requirement makes them necessary. Confirm state authority, trust boundaries, ambiguous outcomes, and operations before presenting a more elaborate ASCII diagram. This anchor is a **thinking framework**, not a fixed platform blueprint.

## How the design changes under a different constraint

For purely advisory fraud signals, asynchronous analysis may be valid; for inline blocking decisions, it is not a drop-in substitute.

**Tutor follow-through:** Explain each architectural choice with one alternative and a trigger for revisiting it. Do not quiz the learner or invent product-specific numbers. For the complete teaching sequence, use `sdt-method-template.md`.
