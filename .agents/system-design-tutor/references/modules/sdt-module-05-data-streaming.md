# Tutor Module 5 — Data Architecture and Streaming

**Routing identity:** `sdt-module-05-data-streaming.md` (match filename even when directory paths are unavailable).

**Load policy:** Use this module only for its own cases or when a specific shared pattern is necessary. Use `sdt-catalog.md` to identify a design; load one anchor file only for an anchor case. For a non-anchor case, derive the worked example using the case's documented architectural choice and `sdt-method-template.md`. Do not imply that the source plan provides complete designs for all 73 cases.

## Anchor files associated with this module

- **Case 42 — Search and indexing service:** `sdt-anchor-12-search-indexing.md`
- **Case 40 — Streaming analytics pipeline:** `sdt-anchor-13-streaming-analytics.md`

## Source-derived domain reference

The following section preserves the input roadmap's domain case selection, architectural choices and teaching notes. This is educational reference material, not a claim about any employer's actual systems or interview content.

## 7. Module 5 — Data Architecture and Streaming

|  # | Design problem                | Main architectural choice                                |
|---:|-------------------------------|----------------------------------------------------------|
| 39 | Event ingestion pipeline      | Brokers, partitions, ordering keys, schema evolution     |
| 40 | Real-time analytics dashboard | Stream aggregations, materialized views, freshness SLA   |
| 41 | Metrics and log platform      | High-cardinality cost, time-series storage, retention    |
| 42 | Search indexing pipeline      | Source DB vs. derived index; update lag and rebuild      |
| 43 | Change Data Capture           | Database log tailing vs. application dual writes         |
| 44 | Data warehouse ETL/ELT        | OLTP vs. OLAP, batch vs. incremental, lineage            |
| 45 | Immutable audit trail         | Tamper resistance, sequence, retention, access controls  |
| 46 | Customer 360 profile          | Identity matching, source-of-truth ownership, privacy    |
| 47 | Data retention and deletion   | Policy propagation, legal holds, backups, audit evidence |

### Concepts in context

- **OLTP:** short operational reads/writes, often transactional; **OLAP:** large
  analytical scans and aggregations.
- **CDC:** propagate committed database changes through a log rather than trying
  to write to two systems in one request.
- **Materialized view:** precomputed read model, with declared staleness and
  rebuild strategy.
- **Event time vs. processing time:** late/out-of-order events can affect
  aggregates; watermarks and correction policy matter.
- **Data lineage:** know which source, transformation and policy produced a
  result.

## Applying this module to a requested case

1. Begin from the exact case's choice/trade-off in the table above; determine what business invariant and user journey make it relevant.
2. Start with one minimal system and an ASCII flow; do not assume microservices, cross-region writes or complex event infrastructure without a constraint.
3. Show at least one credible alternative and its downside; label all invented traffic and latency numbers illustrative.
4. Trace a success path plus the failure path implied by the case's central risk. Recover explicitly from duplicate/reordered/timeout events where they apply.
5. Add security, costs, ownership, DR and migration when they change the architectural decision.
6. Prefer the separate anchor reference for deep cases, or use `sdt-method-template.md` for non-anchor cases. No quizzes or assessments.
