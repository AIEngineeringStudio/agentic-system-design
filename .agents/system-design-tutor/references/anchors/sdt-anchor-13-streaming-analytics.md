# Anchor 13 — Streaming analytics pipeline

**Catalog case:** 40 — Real-time analytics dashboard. **Primary module:** `sdt-module-05-data-streaming.md`. **Optional shared concept:** `sdt-concept-02-messaging-workflows.md`. This is an **illustrative worked reference**: requirements, contracts and vendor details must be adapted to the user scenario.

## 1. Problem and scope

Ingest events from many producers and provide near-real-time aggregated metrics while retaining replay and late-event correction capability.

## 2. Functional requirements

Publish schema-versioned events; validate/deduplicate; calculate windowed aggregates; present a dashboard; reprocess historical input.

## 3. Ranked non-functional constraints

Event completeness, observable freshness, bounded end-to-end lag, cost-managed retention.

## 4. Workload and assumptions

Event rate, cardinality, allowed lateness, exactly which aggregates and retention policies are not assumed.

## 5. Contracts and error semantics

Producer event schema(event_id, producer, key, event_time, schema_version, data); dashboard query(metric, window, dimensions).

## 6. State model and invariant

Durable event log; stream checkpoints; aggregate keyed by window/dimensions; raw archive/replay sources.

## 7. Minimum viable architecture (ASCII)

```text
Producers -> Event broker -> Stream processors -> Aggregate store -> Dashboard API
                  |                 |
               Raw archive      Watermark/checkpoints
```

## 8. Requirements -> decisions -> trade-offs

1. Partition by a key that preserves the ordering required for each computation.
2. Use event-time windows when business timestamps matter; define watermark and correction logic for late records.
3. Maintain derived materialized aggregates separately from canonical raw events.

## 9. Critical execution paths

**Successful flow:** Validate schema -> persist event -> process with durable checkpoint -> update aggregate -> expose freshness status.

**Failure / retry / recovery:** Consumer replays must not inflate counts; out-of-order events trigger updates within permitted lateness; poison events go to visible quarantine.

## 10. Scale, security and enterprise review

**Scale and reliability:** Control high-cardinality dimensions, state-store growth, retention/storage tiering and partition skew; instrument processing lag and cost.

**Enterprise and operational readiness:** Schema ownership, lineage, PII classification, deletion/retention policy, alerting and replay authorization.

## 11. Final architecture and limitations

Start from the above baseline. Add specialized gateways, caches, partitions, secondary indexes, extra regions or queues only when a named requirement makes them necessary. Confirm state authority, trust boundaries, ambiguous outcomes, and operations before presenting a more elaborate ASCII diagram. This anchor is a **thinking framework**, not a fixed platform blueprint.

## How the design changes under a different constraint

If freshness of hours or days is fine, scheduled batch aggregation may be simpler and cheaper.

**Tutor follow-through:** Explain each architectural choice with one alternative and a trigger for revisiting it. Do not quiz the learner or invent product-specific numbers. For the complete teaching sequence, use `sdt-method-template.md`.
