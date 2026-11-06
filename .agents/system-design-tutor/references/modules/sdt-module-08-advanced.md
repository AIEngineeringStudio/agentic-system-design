# Tutor Module 8 — Advanced Architecture Breadth

**Routing identity:** `sdt-module-08-advanced.md` (match filename even when directory paths are unavailable).

**Load policy:** Use this module only for its own cases or when a specific shared pattern is necessary. Use `sdt-catalog.md` to identify a design; load one anchor file only for an anchor case. For a non-anchor case, derive the worked example using the case's documented architectural choice and `sdt-method-template.md`. Do not imply that the source plan provides complete designs for all 73 cases.

## Anchor files associated with this module

- No separate full-depth anchor assigned in this module; derive using the shared method.

## Source-derived domain reference

The following section preserves the input roadmap's domain case selection, architectural choices and teaching notes. This is educational reference material, not a claim about any employer's actual systems or interview content.

## 10. Module 8 — Advanced Architecture Breadth

|  # | Design problem           | Main architectural choice                                 |
|---:|--------------------------|-----------------------------------------------------------|
| 66 | Online ML inference      | Feature store freshness, serving latency, safe fallback   |
| 67 | Recommendation system    | Candidate retrieval vs. ranking, online/offline features  |
| 68 | Enterprise RAG assistant | Retrieval permissions, data leakage prevention, grounding |
| 69 | Nearby location search   | Spatial indices, cell systems, precision vs. cost         |
| 70 | Collaborative editing    | OT vs. CRDT, ordering, offline merge                      |
| 71 | Real-time ad auction     | Tight latency budget, scoring, budget enforcement         |
| 72 | IoT telemetry platform   | Device identity, ingestion bursts, ordering, retention    |
| 73 | Media transcoding        | Asynchronous job graph, retries, storage lifecycle        |

**Treatment:** Pattern-focused unless a case introduces a genuinely new
architecture choice. These extend breadth; they do not replace the financial and
enterprise core.

## Applying this module to a requested case

1. Begin from the exact case's choice/trade-off in the table above; determine what business invariant and user journey make it relevant.
2. Start with one minimal system and an ASCII flow; do not assume microservices, cross-region writes or complex event infrastructure without a constraint.
3. Show at least one credible alternative and its downside; label all invented traffic and latency numbers illustrative.
4. Trace a success path plus the failure path implied by the case's central risk. Recover explicitly from duplicate/reordered/timeout events where they apply.
5. Add security, costs, ownership, DR and migration when they change the architectural decision.
6. Prefer the separate anchor reference for deep cases, or use `sdt-method-template.md` for non-anchor cases. No quizzes or assessments.
