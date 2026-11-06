# Anchor 16 — Legacy modernization

**Catalog case:** 62 — Mainframe modernization. **Primary module:** `sdt-module-07-enterprise.md`. **Optional shared concept:** `sdt-concept-04-security-operations.md`. This is an **illustrative worked reference**: requirements, contracts and vendor details must be adapted to the user scenario.

## 1. Problem and scope

Replace or extend a legacy/mainframe capability incrementally without losing transaction correctness or causing an unsafe cutover.

## 2. Functional requirements

Expose stable APIs; route selected use cases to new implementation; replicate/check data; observe differences; roll back safely.

## 3. Ranked non-functional constraints

Business continuity, state correctness, safe migration/reversibility and organizational ownership.

## 4. Workload and assumptions

Legacy contract, batch windows, state ownership, regulatory controls, latency and vendor limitations must be gathered.

## 5. Contracts and error semantics

Anti-corruption facade with versioned canonical contract; adapter to legacy protocols; validation/dual-run comparison events.

## 6. State model and invariant

Source-of-truth assignment per migrated capability; mapping of legacy keys to new identifiers; replay/validation log; migration checkpoints.

## 7. Minimum viable architecture (ASCII)

```text
Consumers -> Stable facade/anti-corruption layer -> Legacy adapter -> Mainframe
                         |
                         +-> New service -> New data store
                              |
                         Comparison/reconciliation + cutover controller
```

## 8. Requirements -> decisions -> trade-offs

1. Use a strangler migration: replace one bounded capability at a time rather than big-bang rewrite.
2. Keep one writer/authoritative owner per migrated entity during dual-run where possible; uncontrolled dual writes create drift.
3. Parallel read/compare tests expose mapping errors before changing real business effects.

## 9. Critical execution paths

**Successful flow:** Document existing contract -> introduce facade -> mirror/compare permitted reads -> migrate bounded function -> verify transactions -> shift traffic -> retire old path.

**Failure / retry / recovery:** Data divergence is captured and reconciled; any automated rollback must consider writes already made under new ownership. Preserve replay logs and operator decision point.

## 10. Scale, security and enterprise review

**Scale and reliability:** Manage data backfill lag, downstream dependency inventory, dual-run resource cost and state transition consistency under load.

**Enterprise and operational readiness:** Budget for organizational change, training, legacy ownership, vendor contracts, security review, cutover windows and postmigration runbooks.

## 11. Final architecture and limitations

Start from the above baseline. Add specialized gateways, caches, partitions, secondary indexes, extra regions or queues only when a named requirement makes them necessary. Confirm state authority, trust boundaries, ambiguous outcomes, and operations before presenting a more elaborate ASCII diagram. This anchor is a **thinking framework**, not a fixed platform blueprint.

## How the design changes under a different constraint

If legacy system cannot emit reliable change events, use controlled batch/backfill and cutover freezes rather than claiming zero-lag dual-write replication.

**Tutor follow-through:** Explain each architectural choice with one alternative and a trigger for revisiting it. Do not quiz the learner or invent product-specific numbers. For the complete teaching sequence, use `sdt-method-template.md`.
