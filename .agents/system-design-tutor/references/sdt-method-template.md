# Reusable System Design Case Method

Use alongside `SKILL.md`. This is a **design derivation template**, not a list of compulsory headings for every answer.

1. **Problem** — actors, critical user journey, boundary and out-of-scope work.
2. **Functions** — essential commands and reads, error behavior and supported states.
3. **Quality constraints** — explicitly order correctness, security, latency, availability, throughput and cost.
4. **Workload** — requests/sec, burst multiplier, storage and data retention: only grounded or clearly illustrative assumptions.
5. **Contracts** — sample endpoints/events, ownership, auth, replay, idempotency and compatible versioning.
6. **State/invariants** — source of truth, data model, concurrency control, recovery behavior.
7. **Baseline ASCII architecture** — simplest correct implementation with named synchronous boundaries.
8. **Architectural decisions** — for each, state constraint -> options -> selection -> failure/cost introduced -> when to change.
9. **Critical traces** — success -> timeout -> duplicate -> out-of-order -> partial failure -> recovery, if applicable.
10. **Scale and enterprise** — bottlenecks, backpressure, monitoring, SLOs, trust, DR, operational ownership, rollout, cost.
11. **Revised ASCII architecture** — only justified components added; explicit limitations.
12. **What would change** — 2–3 meaningful constraint changes, without asking the learner to answer.

## Response modes

- **Explain concept:** 2–5 paragraphs or a concise table, followed by one small example.
- **Walk me through:** stage architecture progressively. Move to the next stage when requested; no pop quizzes.
- **Design X:** full requirements-to-design treatment. A concept should appear immediately before its first meaningful use.
- **Compare X and Y:** requirements, options, failure-mode trade-offs, and choice conditions. Avoid generic checklists.
- **Review a design:** critique incorrect invariants first, then data and failure flows, then performance and operations. Distinguish confirmed defects from risk/unknowns.

## Recommended decision table

| Requirement/invariant | Candidate A | Candidate B | Choice and why | Hidden cost/revisit trigger |
|---|---|---|---|---|
| Replace with problem-specific facts | ... | ... | ... | ... |

## Source and quality boundary

The input roadmap is a learning plan, not a service specification or a verified collection of employer interview questions. Use sample API shapes and state transitions as illustrative, not external guarantees. For claims about current vendor products or industry standards, check official docs when available and cite them in the explanation.
