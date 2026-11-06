# Messaging and Event-Driven Systems

This reference covers broker-mediated messaging and cross-process delivery.
For an in-process bounded queue and workers, use the
[concurrency reference](08-concurrency.md).

## Producer / Consumer

### Lab

```text
Producer → Queue → Consumer
```

Introduce bounded capacity and failure.

Teach:
- backpressure;
- acknowledgement;
- retry;
- throughput;
- shutdown.

---

## Message Queue

Teach:
- enqueue;
- receive;
- acknowledgement;
- redelivery;
- visibility/lease concepts;
- poison messages.

Use broker-neutral language first.

---

## Publish / Subscribe

### Lab

```text
OrderPlaced
  ├→ Email
  ├→ Inventory
  └→ Analytics
```

Compare with Observer:
- Observer is commonly direct/in-process.
- Pub/Sub commonly uses mediation and may cross processes.

---

## Delivery Semantics

Teach:
- at-most-once;
- at-least-once;
- duplicates;
- deduplication;
- why end-to-end "exactly once" claims need careful qualification.

In interactive lessons, check understanding before advancing to dependent
messaging topics. In complete guides, explain these semantics before using them.

---

## Idempotent Consumer

### Lab
Deliver the same `ChargePayment` or `ReserveInventory` message twice.

The second delivery must not duplicate the business effect.

Teach:
- idempotency key;
- processed-message table;
- business-key dedupe;
- transaction boundary.

---

## Message Ordering

### Lab
Deliver:
- `OrderCreated`
- `OrderCancelled`

out of order.

Teach:
- partition/key ordering;
- sequence numbers;
- stale event rejection;
- commutative operations where possible.

---

## Dead Letter Queue

Create poison messages and define an operational recovery workflow.

A DLQ without investigation/replay procedures is incomplete.

---

## Competing Consumers

Run several consumers against one queue.

Observe:
- throughput;
- duplicate delivery;
- ordering;
- concurrency.

---

## Transactional Outbox

Use the [distributed-systems reference](07-distributed-systems.md) after
covering delivery semantics and idempotency.
