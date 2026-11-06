# Anchor 11 — News feed

**Catalog case:** 24 — Social media feed. **Primary module:** `sdt-module-03-scalable-apps.md`. **Optional shared concept:** `sdt-concept-03-scale-performance.md`. This is an **illustrative worked reference**: requirements, contracts and vendor details must be adapted to the user scenario.

## 1. Problem and scope

Generate a social feed combining posts from followed authors while supporting celebrities and high read traffic.

## 2. Functional requirements

Publish post; follow/unfollow; request ranked/chronological feed; delete or hide content; paginate safely.

## 3. Ranked non-functional constraints

Fast feed reads, acceptable freshness, privacy filtering, controlled write amplification.

## 4. Workload and assumptions

Follower distribution, ranking policy and acceptable staleness determine fan-out choice.

## 5. Contracts and error semantics

POST /posts; GET /feed?cursor=; follow/unfollow API; content visibility policy.

## 6. State model and invariant

Posts (canonical); Follows graph; Feed projection per user (optional); ranking/visibility metadata.

## 7. Minimum viable architecture (ASCII)

```text
Author -> Post service -> Post store -> Fan-out stream -> Home feed projections
                                                       |
Viewer -> Feed API -------------------------> Merge/rank + privacy filter
                                                       |
                                            Read celebrity posts on demand
```

## 8. Requirements -> decisions -> trade-offs

1. Fan-out on write gives cheap reads for ordinary accounts but expensive writes for celebrity followers.
2. Hybrid strategy writes ordinary posts into followers feeds and merges large accounts at read time.
3. Cache derived feeds with explicit invalidation and final visibility rechecks.

## 9. Critical execution paths

**Successful flow:** Persist post -> publish event -> update eligible projections -> on read merge/rank/filter and paginate.

**Failure / retry / recovery:** Projection delay means temporarily stale feed; tolerate/rebuild on replay. Deletes and blocked relationships require strong visibility filtering even if stale projection still contains item.

## 10. Scale, security and enterprise review

**Scale and reliability:** Shard post and feed projections by keys, handle follower skew, set bounded fan-out, monitor feed freshness and recomputation.

**Enterprise and operational readiness:** Content moderation/retention policy, abuse controls, data ownership and cost of storing fan-out copies.

## 11. Final architecture and limitations

Start from the above baseline. Add specialized gateways, caches, partitions, secondary indexes, extra regions or queues only when a named requirement makes them necessary. Confirm state authority, trust boundaries, ambiguous outcomes, and operations before presenting a more elaborate ASCII diagram. This anchor is a **thinking framework**, not a fixed platform blueprint.

## How the design changes under a different constraint

Chronological timelines are simpler than personalized ranking; ranking adds feature freshness and explainability needs.

**Tutor follow-through:** Explain each architectural choice with one alternative and a trigger for revisiting it. Do not quiz the learner or invent product-specific numbers. For the complete teaching sequence, use `sdt-method-template.md`.
