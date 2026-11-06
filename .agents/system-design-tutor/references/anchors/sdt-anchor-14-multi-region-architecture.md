# Anchor 14 — Multi-region architecture

**Catalog case:** 49 — Active-passive failover. **Primary module:** `sdt-module-06-reliability.md`. **Optional shared concept:** `sdt-concept-04-security-operations.md`. This is an **illustrative worked reference**: requirements, contracts and vendor details must be adapted to the user scenario.

## 1. Problem and scope

Serve an important service across regions while meeting explicit failure recovery targets without corrupting state.

## 2. Functional requirements

Serve traffic; replicate data; detect regional degradation; fail over; recover/reconcile; fail back safely.

## 3. Ranked non-functional constraints

Correctness under partition/failover, agreed RPO/RTO, data residency, then latency/cost.

## 4. Workload and assumptions

Workload type, consistency, active-passive/active-active requirement, and recovery goals must be explicitly set.

## 5. Contracts and error semantics

Regional API endpoints with health signals; replication and failover controller; documented operator cutover procedure.

## 6. State model and invariant

Primary or write ownership record; replicated DB; sequence/log position; recovery audit and reconciliation status.

## 7. Minimum viable architecture (ASCII)

```text
Clients -> Global routing -> Region A API -> Primary state
                          |                    |
                          +----> Region B API -> Replica/failover state
                                (controlled promotion)
```

## 8. Requirements -> decisions -> trade-offs

1. Begin with single-writer/active-passive when RTO permits and state correctness matters.
2. Use active-active only if product requirements justify conflict resolution/coordination.
3. Application health, replication lag and safe promotion are distinct from simple DNS failover.

## 9. Critical execution paths

**Successful flow:** Normal writes go to designated owner; replicas serve permitted reads; runbooks and tests ensure controlled promotion.

**Failure / retry / recovery:** Split-brain promotion can create two writers; use fencing/lease or consensus-based authority. Replica lag drives possible data loss; detect/reconcile divergent writes.

## 10. Scale, security and enterprise review

**Scale and reliability:** Measure replication lag, regional capacity and failover time; load-test surviving region at full traffic; verify restoration from backup independently.

**Enterprise and operational readiness:** Document RPO/RTO, regulatory data boundaries, tested DR, incident commander roles, failback/rollback and ongoing multi-region cost.

## 11. Final architecture and limitations

Start from the above baseline. Add specialized gateways, caches, partitions, secondary indexes, extra regions or queues only when a named requirement makes them necessary. Confirm state authority, trust boundaries, ambiguous outcomes, and operations before presenting a more elaborate ASCII diagram. This anchor is a **thinking framework**, not a fixed platform blueprint.

## How the design changes under a different constraint

For read-only workloads, multi-region replicas are simpler; globally coordinated transactions require a different architecture.

**Tutor follow-through:** Explain each architectural choice with one alternative and a trigger for revisiting it. Do not quiz the learner or invent product-specific numbers. For the complete teaching sequence, use `sdt-method-template.md`.
