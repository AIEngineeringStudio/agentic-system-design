# Distributed-System Patterns

## Teaching Rule

Distributed patterns must be taught through failures.

Happy-path-only examples are insufficient.

---

## Timeout

Every remote call may:
- succeed;
- fail;
- become unacceptably slow.

Teach time budgets and cancellation where available.

---

## Retry

Prerequisite: Timeout.

Teach:
- transient vs permanent failure;
- max attempts;
- exponential backoff;
- jitter;
- retry budgets;
- idempotency.

Failure exercise:
simulate many clients retrying at once and discuss retry storms.

---

## Circuit Breaker

Prerequisites:
- remote call failures;
- Timeout;
- Retry.

State model:

```text
Closed → Open → Half-Open → Closed
```

Teach protection of both caller and dependency.

---

## Bulkhead

Partition resources:
- thread/worker pools;
- connection pools;
- concurrency slots.

Goal:
one dependency/workload cannot exhaust everything.

---

## Rate Limiting / Throttling

Teach:
- fixed window;
- sliding window;
- token bucket.

Lab:
per-user / per-tenant / per-endpoint limits.

---

## Transactional Outbox

### Start with dual-write failure

```text
1. commit Order
2. publish OrderCreated
```

Crash between steps.

### Derive

```text
DB transaction:
  Order
  OutboxMessage
```

Separate publisher sends outbox rows.

Teach:
- duplicate publication;
- consumer idempotency;
- ordering;
- cleanup.

---

## Saga

### Lab

```text
Create Order
→ Reserve Inventory
→ Charge Payment
→ Arrange Shipping
```

Inject payment failure.

Derive compensating actions.

Teach:
- choreography;
- orchestration;
- compensation limitations;
- observability.

---

## CQRS

Introduce only when read and write models have genuinely conflicting needs.

Minimal idea:

```text
Commands → change state
Queries  → read state
```

Do not require:
- microservices;
- Event Sourcing;
- multiple databases.

---

## Event Sourcing

Start with events as persisted facts, append-only storage, and rebuilding state
by replay. CQRS is a useful comparison, not a required companion. If the example
uses asynchronous projections or distributed consumers, first cover delivery,
idempotency, ordering, and eventual consistency.

Teach:
- event log as source of truth;
- projections;
- replay;
- schema evolution;
- snapshots;
- temporal queries;
- operational complexity.

Do not present it as a default persistence strategy.

---

## API Gateway

Teach edge concerns:
- routing;
- auth;
- throttling;
- aggregation.

Discuss bottleneck/god-gateway risk.

---

## Backend for Frontend

Use when clients have materially different API needs.

Lab:
- web;
- mobile;
- partner API.

---

## Anti-Corruption Layer

Protect the internal domain from a legacy/external model.

Lab:
vendor fulfillment API with incompatible terminology.

---

## Strangler Fig

Teach incremental legacy replacement through routing/migration boundaries.

---

## Database per Service

Teach:
- ownership;
- autonomy;
- cross-service queries;
- eventual consistency;
- reporting trade-offs.

Do not equate logical ownership with necessarily separate physical servers.
