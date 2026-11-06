# Anchor 12 — Search and indexing service

**Catalog case:** 42 — Search indexing pipeline. **Primary module:** `sdt-module-05-data-streaming.md`. **Optional shared concept:** `sdt-concept-02-messaging-workflows.md`. This is an **illustrative worked reference**: requirements, contracts and vendor details must be adapted to the user scenario.

## 1. Problem and scope

Maintain a searchable index derived from operational records and provide fast query results despite indexing lag.

## 2. Functional requirements

Write authoritative records; index changes; query/search; support incremental updates, deletes and index rebuild.

## 3. Ranked non-functional constraints

Correct document ownership/visibility, declared index freshness, query latency and recoverable reindexing.

## 4. Workload and assumptions

Query language, stemming/locale, ranking goals and allowed staleness come from requirements.

## 5. Contracts and error semantics

Operational API writes to source DB; CDC/outbox record stream; GET /search?q=&cursor=; index status/rebuild controls.

## 6. State model and invariant

Source records with revision/version; index documents with source_id, revision and visibility; checkpoint/replay offsets.

## 7. Minimum viable architecture (ASCII)

```text
Source API -> Canonical DB -> CDC/outbox -> Indexer workers -> Search index
                                                         |                |
                                                   Checkpoint log      Query API
```

## 8. Requirements -> decisions -> trade-offs

1. Treat search index as a derived read model, not source of truth.
2. Choose log/CDC capture rather than fragile application dual-write.
3. Apply source version/order to avoid delayed stale updates resurrecting deleted documents.

## 9. Critical execution paths

**Successful flow:** Commit canonical write -> emit captured change -> upsert indexed revision -> query returns results after declared lag.

**Failure / retry / recovery:** Indexer outage accumulates lag. At-least-once replay is idempotent by document version; full rebuild from canonical source with atomic index swap where appropriate.

## 10. Scale, security and enterprise review

**Scale and reliability:** Shard index by query/document needs, account for high cardinality, limit indexing throughput and measure freshness and search misses.

**Enterprise and operational readiness:** Recheck document access permissions, enforce deletion requirements, define data lineage and operator runbooks.

## 11. Final architecture and limitations

Start from the above baseline. Add specialized gateways, caches, partitions, secondary indexes, extra regions or queues only when a named requirement makes them necessary. Confirm state authority, trust boundaries, ambiguous outcomes, and operations before presenting a more elaborate ASCII diagram. This anchor is a **thinking framework**, not a fixed platform blueprint.

## How the design changes under a different constraint

If search must include uncommitted latest writes, augment the index with direct source reads or a stronger write/query contract.

**Tutor follow-through:** Explain each architectural choice with one alternative and a trigger for revisiting it. Do not quiz the learner or invent product-specific numbers. For the complete teaching sequence, use `sdt-method-template.md`.
