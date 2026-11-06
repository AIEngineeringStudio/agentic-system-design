# System Design Tutor — Exact Case and Anchor Router

**Routing rule:** identify the closest exact case or user-described behavior, then load only its module file and (if assigned) its individual anchor. A keyword may have multiple plausible domains; use the surrounding requirements. File lookup matches either `references/.../<filename>` or uploaded flat `<filename>`.

## Alias shortcuts

| Request phrase | Preferred resolution |
|---|---|
| payment authorization | Case 1, Card authorization anchor 01 |
| credit card authorization | Case 1, Card authorization anchor 01 |
| authorize payment | Case 1; if asking about identity authorization instead, use Case 59 |
| payments gateway | Case 2, Payment gateway anchor 05 |
| card payment gateway | Case 2, Payment gateway anchor 05 |
| ledger | Case 5, Double-entry ledger anchor 02 |
| accounting ledger | Case 5, Double-entry ledger anchor 02 |
| fraud scoring | Case 10, Fraud decisioning anchor 04 |
| ratelimiter | Case 18, Distributed rate limiter anchor 06 |
| rate limiting | Case 18, Distributed rate limiter anchor 06 |
| notifications | Case 20, Notification service anchor 09 |
| chat app | Case 23, Chat anchor 10 |
| WhatsApp | Case 23, Chat anchor 10 |
| timeline / feed | Case 24, News feed anchor 11 |
| checkout / shopping cart | Case 28, E-commerce checkout anchor 07 |
| booking seats | Case 30, Ticket booking anchor 08 |
| Saga orchestration | Case 32 or 36, Module 04; optionally anchor 07 for checkout |
| outbox pattern | Case 37, Module 04 and messaging concept |
| CDC | Case 43, Module 05 and messaging concept |
| stream processing | Case 39–40, Module 05; anchor 13 for dashboards/analytics |
| search indexing | Case 42, Search/indexing anchor 12 |
| high availability / failover | Cases 48–53, Module 06; anchor 14 for multi-region |
| multi region | Cases 48–50, Module 06; anchor 14 for DR |
| SSO / single sign-on | Case 57, Enterprise IAM anchor 15 |
| access management | Cases 57–59, Module 07; anchor 15 |
| mainframe / legacy migration | Case 62, Legacy modernization anchor 16 |
| RAG assistant | Case 68, Module 08 |
| CRDT / collaborative editor | Case 70, Module 08 |

## The complete 73-case registry

### Module 1: Architecture Foundations

**Reference:** `sdt-module-01-foundations.md`

| ID | Design case | Core architectural decision | Optional anchor |
|---:|---|---|---|
Foundations are 20 reusable concepts rather than numbered case studies. Read this module for general architectural concepts, or in support of a case-specific explanation.

### Module 2: Payments and Financial Systems

**Reference:** `sdt-module-02-payments.md`

| ID | Design case | Core architectural decision | Optional anchor |
|---:|---|---|---|
| 1 | Credit-card authorization | Low-latency synchronous decision; idempotency; uncertain responses; risk checks | `sdt-anchor-01-card-authorization.md` |
| 2 | Merchant payment gateway | API authentication, partner integration, retry contracts, provider failures | `sdt-anchor-05-payment-gateway.md` |
| 3 | Capture, clearing and settlement | Different financial phases; batch/event workflows; finality and reconciliation | `sdt-anchor-03-settlement-reconciliation.md` |
| 4 | Multi-provider payment orchestration | Routing, circuit breakers, provider-specific semantics, fallback safety | — |
| 5 | Double-entry financial ledger | Debit/credit invariants; immutable entries; transactional posting; auditability | `sdt-anchor-02-double-entry-ledger.md` |
| 6 | Refunds and reversals | State machine, partial refunds, duplicate requests, external status | — |
| 7 | Chargebacks/disputes | Long-running workflow, deadlines, evidence, exception queues | — |
| 8 | Peer-to-peer transfer | Atomic ledger entries, holds, concurrency, recipient identity | — |
| 9 | Recurring billing/subscriptions | Scheduling, retry policy, failed payments, idempotent cycles | — |
| 10 | Real-time fraud detection | Feature freshness, scoring latency, rules + models, fail-open/closed trade-off | `sdt-anchor-04-fraud-decisioning.md` |
| 11 | Limits and velocity controls | Atomic counters, sliding windows, hot accounts, correct risk decisions | — |
| 12 | Merchant onboarding / KYC | Human reviews, third-party checks, long-lived durable orchestration | — |
| 13 | Reconciliation engine | Match ledgers to external files/events; discrepancies; reprocessing | — |
| 14 | Transaction notifications | Outbox, event consumers, delivery retries, user preferences | — |
| 15 | Rewards / loyalty points | Earn/burn events, balances, expiry, reversals and consistency | — |
| 16 | Card tokenization vault | Sensitive data isolation, tokens, HSM/KMS, audit and access boundaries | — |

### Module 3: Scalable Distributed Applications

**Reference:** `sdt-module-03-scalable-apps.md`

| ID | Design case | Core architectural decision | Optional anchor |
|---:|---|---|---|
| 17 | URL shortener | Unique IDs, key-value lookup, redirects, hot-key caching | — |
| 18 | Distributed rate limiter | Token bucket vs. sliding window; atomic distributed counters | `sdt-anchor-06-distributed-rate-limiter.md` |
| 19 | API gateway | Authentication boundary, routing, rate limits, request policies | — |
| 20 | Multi-channel notifications | Fan-out, queue vs. stream, retries, dead-letter handling | `sdt-anchor-09-notification-service.md` |
| 21 | Distributed job scheduler | Leader election, claiming work, duplicate-safe execution | — |
| 22 | Webhook delivery platform | Delivery contracts, signed payloads, retry windows, backoff | — |
| 23 | WhatsApp-style chat | WebSocket vs. polling, ordering, offline delivery, fan-out | `sdt-anchor-10-chat.md` |
| 24 | Social media feed | Fan-out on write vs. fan-out on read, celebrity skew | `sdt-anchor-11-news-feed.md` |
| 25 | Search autocomplete | Prefix index/trie, ranking, freshness, cache | — |
| 26 | File sharing | Object storage, metadata DB, pre-signed URLs, authorization | — |
| 27 | Video streaming | Transcoding jobs, CDN, segments, adaptive bitrate | — |
| 28 | E-commerce checkout | State transitions, reservation, payment, order Saga | `sdt-anchor-07-ecommerce-checkout.md` |

### Module 4: Distributed Transactions and Workflows

**Reference:** `sdt-module-04-workflows.md`

| ID | Design case | Core architectural decision | Optional anchor |
|---:|---|---|---|
| 29 | Inventory reservation | Atomic stock decrement, TTL reservations, expiry races | — |
| 30 | Ticket booking | Optimistic vs. pessimistic locking; unique seat constraints | `sdt-anchor-08-ticket-booking.md` |
| 31 | Driver-to-rider matching | Geospatial index, freshness, claim ownership, concurrency | — |
| 32 | Order fulfillment | Saga orchestration vs. choreography; compensating actions | — |
| 33 | Coupon redemption | Global limits, per-user uniqueness, hot keys | — |
| 34 | Wallet balance | Immutable ledger vs. mutable read model; concurrent spending | — |
| 35 | Shipment tracking | Event ingestion, out-of-order events, eventual consistency | — |
| 36 | Durable workflow engine | State machines, timers, retries, cancellation and recovery | — |
| 37 | Transactional outbox | Atomic data update + durable event intent; relay deduplication | — |
| 38 | Idempotent consumer | At-least-once events, inbox table, replay-safe side effects | — |

### Module 5: Data Architecture and Streaming

**Reference:** `sdt-module-05-data-streaming.md`

| ID | Design case | Core architectural decision | Optional anchor |
|---:|---|---|---|
| 39 | Event ingestion pipeline | Brokers, partitions, ordering keys, schema evolution | — |
| 40 | Real-time analytics dashboard | Stream aggregations, materialized views, freshness SLA | `sdt-anchor-13-streaming-analytics.md` |
| 41 | Metrics and log platform | High-cardinality cost, time-series storage, retention | — |
| 42 | Search indexing pipeline | Source DB vs. derived index; update lag and rebuild | `sdt-anchor-12-search-indexing.md` |
| 43 | Change Data Capture | Database log tailing vs. application dual writes | — |
| 44 | Data warehouse ETL/ELT | OLTP vs. OLAP, batch vs. incremental, lineage | — |
| 45 | Immutable audit trail | Tamper resistance, sequence, retention, access controls | — |
| 46 | Customer 360 profile | Identity matching, source-of-truth ownership, privacy | — |
| 47 | Data retention and deletion | Policy propagation, legal holds, backups, audit evidence | — |

### Module 6: Scalability, Cloud and Reliability

**Reference:** `sdt-module-06-reliability.md`

| ID | Design case | Core architectural decision | Optional anchor |
|---:|---|---|---|
| 48 | Multi-region read service | Replicas, latency routing, stale-read tolerance | — |
| 49 | Active-passive failover | Regional recovery, replicated state, cutover procedure | `sdt-anchor-14-multi-region-architecture.md` |
| 50 | Active-active transactions | Write coordination, conflict resolution, partition tolerance | — |
| 51 | Distributed cache tier | Cache-aside, TTL, consistency, stampede prevention | — |
| 52 | Flash-sale traffic | Admission control, virtual queues, shed load safely | — |
| 53 | Backup and disaster recovery | RPO, RTO, tested restore, data integrity | — |
| 54 | Circuit breaker and fallback | Timeouts, retry budgets, bulkheads, failure isolation | — |
| 55 | Multi-tenant platform | Isolation, noisy neighbors, cost/accounting boundaries | — |
| 56 | Safe deployment pipeline | Canary/blue-green, compatibility, feature flags, rollback | — |

### Module 7: Security and Enterprise Architecture

**Reference:** `sdt-module-07-enterprise.md`

| ID | Design case | Core architectural decision | Optional anchor |
|---:|---|---|---|
| 57 | Enterprise single sign-on | OIDC/SAML, trust federation, session and token lifetimes | `sdt-anchor-15-enterprise-iam.md` |
| 58 | Multi-factor authentication | Step-up verification, recovery, device trust, risk signals | — |
| 59 | Authorization platform | RBAC vs. ABAC, policy evaluation, revocation | — |
| 60 | Secrets and key management | KMS/HSM, key lifecycle, rotation, least privilege | — |
| 61 | B2B partner API | Contract versioning, mTLS/OAuth, quotas, failure isolation | — |
| 62 | Mainframe modernization | Strangler migration, anti-corruption layer, dual-run validation | `sdt-anchor-16-legacy-modernization.md` |
| 63 | Hybrid-cloud integration | Connectivity, trust boundary, egress, latency and ownership | — |
| 64 | Cardholder-data boundary | Tokenization, segmentation, audit and PCI scope | — |
| 65 | Consent and privacy service | Consent versioning, policy checks, deletion/retention | — |

### Module 8: Advanced Architecture Breadth

**Reference:** `sdt-module-08-advanced.md`

| ID | Design case | Core architectural decision | Optional anchor |
|---:|---|---|---|
| 66 | Online ML inference | Feature store freshness, serving latency, safe fallback | — |
| 67 | Recommendation system | Candidate retrieval vs. ranking, online/offline features | — |
| 68 | Enterprise RAG assistant | Retrieval permissions, data leakage prevention, grounding | — |
| 69 | Nearby location search | Spatial indices, cell systems, precision vs. cost | — |
| 70 | Collaborative editing | OT vs. CRDT, ordering, offline merge | — |
| 71 | Real-time ad auction | Tight latency budget, scoring, budget enforcement | — |
| 72 | IoT telemetry platform | Device identity, ingestion bursts, ordering, retention | — |
| 73 | Media transcoding | Asynchronous job graph, retries, storage lifecycle | — |

## Sixteen deep-dive anchors

| Anchor | Case | Reference filename |
|---:|---|---|
| 01 | 1 — Card authorization | `sdt-anchor-01-card-authorization.md` |
| 02 | 5 — Double-entry ledger | `sdt-anchor-02-double-entry-ledger.md` |
| 03 | 3 — Settlement and reconciliation | `sdt-anchor-03-settlement-reconciliation.md` |
| 04 | 10 — Fraud decisioning | `sdt-anchor-04-fraud-decisioning.md` |
| 05 | 2 — Payment gateway | `sdt-anchor-05-payment-gateway.md` |
| 06 | 18 — Distributed rate limiter | `sdt-anchor-06-distributed-rate-limiter.md` |
| 07 | 28 — E-commerce checkout | `sdt-anchor-07-ecommerce-checkout.md` |
| 08 | 30 — Ticket booking | `sdt-anchor-08-ticket-booking.md` |
| 09 | 20 — Notification service | `sdt-anchor-09-notification-service.md` |
| 10 | 23 — Chat | `sdt-anchor-10-chat.md` |
| 11 | 24 — News feed | `sdt-anchor-11-news-feed.md` |
| 12 | 42 — Search and indexing service | `sdt-anchor-12-search-indexing.md` |
| 13 | 40 — Streaming analytics pipeline | `sdt-anchor-13-streaming-analytics.md` |
| 14 | 49 — Multi-region architecture | `sdt-anchor-14-multi-region-architecture.md` |
| 15 | 57 — Enterprise IAM | `sdt-anchor-15-enterprise-iam.md` |
| 16 | 62 — Legacy modernization | `sdt-anchor-16-legacy-modernization.md` |

## Ambiguity handling

- **Authorization** alone may mean payment authorization (case 1) or access control (case 59); use actor and expected state change.
- **Gateway** alone may mean payment gateway (case 2) or general API gateway (case 19).
- **Events / streaming** may refer to event ingest (case 39), workflow Saga/outbox (cases 32, 37), or analytics (case 40).
- Do not load all possible files. Choose the best user-grounded match and, if truly undecidable, ask one targeted question.
- For cross-module cases, explain exactly why the second concept is needed instead of opening a whole second module.
