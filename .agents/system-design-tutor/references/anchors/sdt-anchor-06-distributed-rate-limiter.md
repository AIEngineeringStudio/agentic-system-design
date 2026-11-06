# Anchor 06 — Distributed rate limiter

**Catalog case:** 18 — Distributed rate limiter. **Primary module:** `sdt-module-03-scalable-apps.md`. **Optional shared concept:** `sdt-concept-03-scale-performance.md`. This is an **illustrative worked reference**: requirements, contracts and vendor details must be adapted to the user scenario.

## 1. Problem and scope

Restrict requests fairly across users, clients or tenants under distributed traffic without creating a fragile central bottleneck.

## 2. Functional requirements

Check/consume a quota; expose remaining allowance/reset policy; change policies; fail safely under storage/service faults.

## 3. Ranked non-functional constraints

Bounded decision latency, consistency of enforcement when required, fairness and availability.

## 4. Workload and assumptions

The required limit (hard security cap vs soft courtesy quota), precision and geographic distribution determine the design.

## 5. Contracts and error semantics

allow(key, cost, policy_id) -> allowed, remaining, retry_after; policies carry window/burst parameters.

## 6. State model and invariant

Counters/token state per scoped key and time window; rate policies with versions; audit for configuration changes.

## 7. Minimum viable architecture (ASCII)

```text
Clients -> API tier -> Rate-limit decision -> Atomic counter store
                     |                  |
                   Request path       Policy/config cache
```

## 8. Requirements -> decisions -> trade-offs

1. Token bucket allows short bursts; sliding windows enforce different fairness at higher state cost.
2. Local per-instance counters are cheap but can exceed global quotas; centralized atomic operations tighten enforcement but raise dependency/latency risk.
3. A key/window design must avoid clock-sensitive ambiguity and hot-tenant contention.

## 9. Critical execution paths

**Successful flow:** Resolve subject and policy -> atomically consume allowance -> allow or reject with meaningful retry hint.

**Failure / retry / recovery:** Simultaneous requests must not race beyond a hard cap. If backing store fails, fail-open/closed behavior is an explicit per-policy choice and must be measured.

## 10. Scale, security and enterprise review

**Scale and reliability:** Shard by keys, protect hot keys, use short-lived policy caches, bound command latency and report enforcement errors separately from allowed traffic.

**Enterprise and operational readiness:** Define who may change quotas, tenant fairness, observability, rate-limit policy governance and outages.

## 11. Final architecture and limitations

Start from the above baseline. Add specialized gateways, caches, partitions, secondary indexes, extra regions or queues only when a named requirement makes them necessary. Confirm state authority, trust boundaries, ambiguous outcomes, and operations before presenting a more elaborate ASCII diagram. This anchor is a **thinking framework**, not a fixed platform blueprint.

## How the design changes under a different constraint

Multi-region enforcement may need bounded overage, local reservation of quota or higher-latency coordination; choose explicitly.

**Tutor follow-through:** Explain each architectural choice with one alternative and a trigger for revisiting it. Do not quiz the learner or invent product-specific numbers. For the complete teaching sequence, use `sdt-method-template.md`.
