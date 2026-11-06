# Tutor Module 6 — Scalability, Cloud and Reliability

**Routing identity:** `sdt-module-06-reliability.md` (match filename even when directory paths are unavailable).

**Load policy:** Use this module only for its own cases or when a specific shared pattern is necessary. Use `sdt-catalog.md` to identify a design; load one anchor file only for an anchor case. For a non-anchor case, derive the worked example using the case's documented architectural choice and `sdt-method-template.md`. Do not imply that the source plan provides complete designs for all 73 cases.

## Anchor files associated with this module

- **Case 49 — Multi-region architecture:** `sdt-anchor-14-multi-region-architecture.md`

## Source-derived domain reference

The following section preserves the input roadmap's domain case selection, architectural choices and teaching notes. This is educational reference material, not a claim about any employer's actual systems or interview content.

## 8. Module 6 — Scalability, Cloud and Reliability

|  # | Design problem               | Main architectural choice                                    |
|---:|------------------------------|--------------------------------------------------------------|
| 48 | Multi-region read service    | Replicas, latency routing, stale-read tolerance              |
| 49 | Active-passive failover      | Regional recovery, replicated state, cutover procedure       |
| 50 | Active-active transactions   | Write coordination, conflict resolution, partition tolerance |
| 51 | Distributed cache tier       | Cache-aside, TTL, consistency, stampede prevention           |
| 52 | Flash-sale traffic           | Admission control, virtual queues, shed load safely          |
| 53 | Backup and disaster recovery | RPO, RTO, tested restore, data integrity                     |
| 54 | Circuit breaker and fallback | Timeouts, retry budgets, bulkheads, failure isolation        |
| 55 | Multi-tenant platform        | Isolation, noisy neighbors, cost/accounting boundaries       |
| 56 | Safe deployment pipeline     | Canary/blue-green, compatibility, feature flags, rollback    |

### Must understand

- **RPO:** maximum acceptable data loss measured in time. **RTO:** maximum
  acceptable recovery time.
- **Availability vs. correctness:** degraded reads may be acceptable; incorrect
  balances or duplicate postings may not be.
- **Backpressure:** reduce accepted work to what downstream systems can process,
  rather than filling unlimited queues.
- **Retry amplification:** nested automatic retries can turn a partial outage
  into a total one; use bounded budgets and jitter.
- **Operational readiness:** dashboards, alerts, runbooks, DR tests, ownership
  and on-call dependencies.

## Applying this module to a requested case

1. Begin from the exact case's choice/trade-off in the table above; determine what business invariant and user journey make it relevant.
2. Start with one minimal system and an ASCII flow; do not assume microservices, cross-region writes or complex event infrastructure without a constraint.
3. Show at least one credible alternative and its downside; label all invented traffic and latency numbers illustrative.
4. Trace a success path plus the failure path implied by the case's central risk. Recover explicitly from duplicate/reordered/timeout events where they apply.
5. Add security, costs, ownership, DR and migration when they change the architectural decision.
6. Prefer the separate anchor reference for deep cases, or use `sdt-method-template.md` for non-anchor cases. No quizzes or assessments.
