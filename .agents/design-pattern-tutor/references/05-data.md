# Data Patterns

## Repository

Use domain-oriented persistence needs.

Start with SQL/ORM calls inside business logic and extract a repository around
the domain's persistence needs. Avoid generic repository ceremony over an ORM
unless it creates a meaningful boundary.

Teach:
- aggregate loading;
- save semantics;
- test boundaries;
- query-model exceptions.

---

## Active Record

### Lab
Simple CRUD model that persists itself.

Teach why it is productive.

Then show where rich domain logic and persistence concerns collide.

---

## Data Mapper

Separate domain object from persistence mapping.

Compare directly with Active Record.

---

## Unit of Work

### Lab
Modify multiple related entities in one application use case.

Teach:
- change tracking;
- transaction boundary;
- commit.

Point out that many ORMs already implement this internally.

---

## Identity Map

Teach when discussing ORM sessions/change tracking.

Question:
> If the same row is loaded twice in one unit of work, should we get two independent domain identities?

---

## Cache-Aside

### Baseline

```text
read key
  ↓
cache?
 ├─ hit → return
 └─ miss → DB → cache → return
```

### Must test
- stale data;
- invalidation;
- expiration;
- cache outage;
- thundering herd;
- read-after-write behavior.

---

## Read Replicas

Teach replication lag and read-after-write anomalies.

---

## Sharding

Prerequisites:
- indexing;
- query planning;
- replication;
- partitioning;
- caching;
- vertical scaling.

Do not present sharding as an early scalability default.

---

## Database per Service

Use the [distributed-systems reference](07-distributed-systems.md) for the
canonical lesson on data ownership and eventual consistency.

---

## Shared Database

Teach comparatively:
- simplicity;
- coupling;
- ownership ambiguity;
- coordinated schema changes.

---

## CQRS / Event Sourcing

Use the [distributed-systems reference](07-distributed-systems.md).
