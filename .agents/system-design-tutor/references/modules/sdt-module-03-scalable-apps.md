# Tutor Module 3 — Scalable Distributed Applications

**Routing identity:** `sdt-module-03-scalable-apps.md` (match filename even when directory paths are unavailable).

**Load policy:** Use this module only for its own cases or when a specific shared pattern is necessary. Use `sdt-catalog.md` to identify a design; load one anchor file only for an anchor case. For a non-anchor case, derive the worked example using the case's documented architectural choice and `sdt-method-template.md`. Do not imply that the source plan provides complete designs for all 73 cases.

## Anchor files associated with this module

- **Case 18 — Distributed rate limiter:** `sdt-anchor-06-distributed-rate-limiter.md`
- **Case 28 — E-commerce checkout:** `sdt-anchor-07-ecommerce-checkout.md`
- **Case 20 — Notification service:** `sdt-anchor-09-notification-service.md`
- **Case 23 — Chat:** `sdt-anchor-10-chat.md`
- **Case 24 — News feed:** `sdt-anchor-11-news-feed.md`

## Source-derived domain reference

The following section preserves the input roadmap's domain case selection, architectural choices and teaching notes. This is educational reference material, not a claim about any employer's actual systems or interview content.

## 5. Module 3 — Scalable Distributed Applications

|  # | Design problem              | Main architectural choice                                       |
|---:|-----------------------------|-----------------------------------------------------------------|
| 17 | URL shortener               | Unique IDs, key-value lookup, redirects, hot-key caching        |
| 18 | Distributed rate limiter    | Token bucket vs. sliding window; atomic distributed counters    |
| 19 | API gateway                 | Authentication boundary, routing, rate limits, request policies |
| 20 | Multi-channel notifications | Fan-out, queue vs. stream, retries, dead-letter handling        |
| 21 | Distributed job scheduler   | Leader election, claiming work, duplicate-safe execution        |
| 22 | Webhook delivery platform   | Delivery contracts, signed payloads, retry windows, backoff     |
| 23 | WhatsApp-style chat         | WebSocket vs. polling, ordering, offline delivery, fan-out      |
| 24 | Social media feed           | Fan-out on write vs. fan-out on read, celebrity skew            |
| 25 | Search autocomplete         | Prefix index/trie, ranking, freshness, cache                    |
| 26 | File sharing                | Object storage, metadata DB, pre-signed URLs, authorization     |
| 27 | Video streaming             | Transcoding jobs, CDN, segments, adaptive bitrate               |
| 28 | E-commerce checkout         | State transitions, reservation, payment, order Saga             |

### Distinct patterns to extract

- **Read-heavy vs. write-heavy:** drives indexing, denormalization, caching and
  partitioning.
- **Push vs. pull:** for chat, feeds and notifications; connection management
  costs matter.
- **Fan-out on write vs. read:** precompute for cheap reads or compute on demand
  for lower write amplification.
- **Queue vs. log:** a work queue distributes tasks; an event log enables
  independent consumers/replay, with product-specific semantics.
- **Object storage vs. database blobs:** separate large content delivery from
  searchable metadata and authorization.

## Applying this module to a requested case

1. Begin from the exact case's choice/trade-off in the table above; determine what business invariant and user journey make it relevant.
2. Start with one minimal system and an ASCII flow; do not assume microservices, cross-region writes or complex event infrastructure without a constraint.
3. Show at least one credible alternative and its downside; label all invented traffic and latency numbers illustrative.
4. Trace a success path plus the failure path implied by the case's central risk. Recover explicitly from duplicate/reordered/timeout events where they apply.
5. Add security, costs, ownership, DR and migration when they change the architectural decision.
6. Prefer the separate anchor reference for deep cases, or use `sdt-method-template.md` for non-anchor cases. No quizzes or assessments.
